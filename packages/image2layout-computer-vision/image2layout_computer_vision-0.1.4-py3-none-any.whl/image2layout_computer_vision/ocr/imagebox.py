# %%
import os
import json
import colorsys
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from ..utils import get_image, AnnoDraw
from typing import Union, Dict, Tuple, List, Any

# %%
class BoxMerge:
    
    @classmethod
    def same_column_match(cls,
                boxa, boxb,
                hdist_max=0.5,
                vdist_max=2.0,
                height_ratio_min=0.8,
                ):
        if boxb[1] < boxa[1]:
            return cls.same_column_match(
                boxb, boxa,
                hdist_max=hdist_max,
                vdist_max=vdist_max,
                height_ratio_min=height_ratio_min,
            )
        
        heights = np.array([boxb[3] - boxb[1], boxa[3] - boxa[1]])
        height_max = max(np.max(heights), 1)
        height_ratio = np.min(heights) / height_max
        
        hdists = np.abs([
            *(boxb - boxa)[[0, 2]],
            boxb[[0, 2]].mean() - boxa[[0, 2]].mean(),
        ])
        vdists = np.abs(boxb - boxa)[[1, 3]]
        # hdist, vdist, height_ratio, height_max
        
        return all([
            np.min(hdists) / height_max < hdist_max,
            np.min(vdists) / height_max < vdist_max,
            height_ratio > height_ratio_min,
        ])
    
    @classmethod
    def box_containing_match(cls, boxa, boxb, area_threshold=0.8):
        _boxes = np.array([boxa, boxb]).reshape(2, 2, 2)
        inter_box = np.concatenate([
            np.max(_boxes[:, 0], axis=0),
            np.min(_boxes[:, 1], axis=0),
        ])
        inter_wh = np.clip(inter_box[2:] - inter_box[:2], 0, None)
        
        inter_area = np.prod(inter_wh)
        areas = np.clip(np.prod(_boxes[:, 1] - _boxes[:, 0], axis=-1), 1.0, None)
        inter_max_ratio = np.max(inter_area / areas)
        return inter_max_ratio >= area_threshold
    
    @classmethod
    def group_texts_by_match_fn(cls, boxes: np.ndarray, fn, sort_index=None, **kwargs):
        # boxes should be sorted
        assert callable(fn)
        assert isinstance(boxes, np.ndarray)
        assert len(boxes.shape) == 2
        assert boxes.shape[-1] == 4
        
        count = len(boxes)
        assert count > 0
        
        if sort_index is None:
            sorted_indices = np.arange(count)
        else:
            assert sort_index in list(range(4))
            sorted_indices = np.argsort(boxes[:, sort_index])
        sorted_indices_reverse  = np.zeros(count, int)
        sorted_indices_reverse[sorted_indices] = np.arange(count)
        
        sorted_boxes = boxes[sorted_indices]
        count = len(sorted_boxes)
        
        matched_indices = set()
        remaining_indices = set(range(count))
        linked_groups = []
        
        for _ in range(count):
            if len(remaining_indices) <= 0:
                break
            
            start_index = min(remaining_indices)
            
            head_index = start_index
            linked_indices = [head_index]
            
            for next_index in range(head_index+1, count):
                if next_index in matched_indices:
                    continue
                if fn(sorted_boxes[head_index], sorted_boxes[next_index], **kwargs):
                    linked_indices.append(next_index)
                    head_index = next_index
            
            linked_groups.append(linked_indices)
            matched_indices.update(linked_indices)
            remaining_indices.difference_update(linked_indices)
        
        data_group = []
        for i, indices in enumerate(linked_groups):
            original_indices = sorted_indices[indices]
            group_box = cls.merge_boxes(sorted_boxes[indices])
            data_group.append({
                'indices': original_indices,
                'box': group_box,
            })
        
        df_group = pd.DataFrame(data_group, columns=['indices', 'box'])
        df_group
        return df_group
    
    @classmethod
    def box_dist(cls, boxa, boxb):
        dists = np.array([
            boxa[:2] - boxb[2:],
            boxb[:2] - boxa[2:],
        ])
        min_idx = np.argmin(np.abs(dists), axis=0)
        return np.array([dists[min_idx[0], 0], dists[min_idx[1], 1]])
    
    @classmethod
    def same_line_align(cls, boxa, boxb) -> float:
        ya = boxa[[1, 3]]
        yb = boxb[[1, 3]]
        if np.prod(yb - ya) < 0:
            # one bounding the other
            return 1.0
        
        inter = np.min([ya[1], yb[1]]) - np.max([ya[0], yb[0]])
        union = np.max([ya, yb]) - np.min([ya, yb])
        iou = float(np.clip(inter / max(union, 1), 0, 1))
        return iou
    
    @classmethod
    def same_line_match(cls,
                boxa:np.ndarray,
                boxb:np.ndarray,
                dist_max:float=1.0,
                dist_min:float=-0.1,
                iou_min:float=0.4,
                ) -> bool:
        dist = cls.box_dist(boxa, boxb)[0]
        max_height = np.clip(np.max([boxa[3] - boxa[1], boxb[3] - boxb[1]]), 1, None)
        dist_ratio = dist / max_height
        if dist_ratio > dist_max:
            return False
        if dist_ratio < dist_min:
            return False
        
        iou = cls.same_line_align(boxa, boxb)
        if iou < iou_min:
            return False
        
        return True
    
    @classmethod
    def merge_boxes(cls, boxes):
        return np.concatenate([
            np.min(boxes[:, :2], axis=0),
            np.max(boxes[:, 2:], axis=0),
        ])

# %%
class ImageBoxes(list):
    mask_color = tuple([0, 0, 0])
    mask_opacity = 0.5
    box_colors = [
        tuple([int(v * 255) for v in colorsys.hsv_to_rgb(i/3, 1.0, 1.0)])
        for i in range(3)
    ]
    def __init__(self,
                boxes:list,
                image=None,
                size=None,
                offset=(0, 0),
                level=0,
                parent=None,
                ):
        '''
        image (PIL.Image.Image RGB): input image
        boxes (list): list of (lists of...) ints for xyxy coordinates
        '''
        
        self.parent = parent
        self.offset = np.array(offset, int)
        self.text = ''
        self.texts = []
        
        if isinstance(boxes, np.ndarray):
            boxes = boxes.tolist()
        assert isinstance(boxes, list), f'`boxes` must be of type [list, np.ndarray], found {type(boxes)}'
        
        self.is_single_instance = len(boxes) == 4 and all([isinstance(v, int) for v in boxes])
        self.image = get_image(image) if image is not None else None
        if self.image is not None:
            self.size = self.image.size
        else:
            assert size is not None
            self.size = size
        self.level = int(level)
        self.children_levels = -1
        self.box = np.array([0, 0, 0, 0], int)
        self.box_outer = np.array([0, 0, 0, 0], int)
        self.box_outer_found = False
        self.boxes = []        # all child-most boxes
        self.boxes_top = []    # top-level (1 level in) boxes
        
        if self.is_single_instance:
            self.children_levels = 0
            self.box = np.array(boxes, int)
            self.box_outer = np.array(self.box, int)
            self.boxes.append(boxes)
            self.boxes_top.append(boxes)
            super().__init__([])
        else:
            imageboxes = []
            for i, box in enumerate(boxes):
                child_imageboxes = ImageBoxes(
                    boxes=box,
                    size=self.size,
                    level=self.level + 1,
                    parent=self,
                )
                imageboxes.append(child_imageboxes)
                self.boxes.extend(child_imageboxes.boxes)
                self.boxes_top.append(child_imageboxes.box_outer.tolist())
                
                if not self.box_outer_found:
                    self.box_outer_found = True
                    self.box_outer = np.array(child_imageboxes.box_outer, int)
                else:
                    self.box_outer[:2] = np.min([self.box_outer[:2], child_imageboxes.box_outer[:2]], axis=0)
                    self.box_outer[2:] = np.max([self.box_outer[2:], child_imageboxes.box_outer[2:]], axis=0)
                
            self.box = np.array(self.box_outer, int)
            super().__init__(imageboxes)
        
        self.update_texts()
    
    def _repr(self) -> list:
        if self.is_single_instance:
            return [f'Box[{",".join([str(v) for v in self.box])}],']
        else:
            return [
                f'Boxes[{len(self)}x](',
                *[
                    f'  {_line}'
                    for child in self
                    for _line in child._repr()
                ],
                ')',
            ]
        
    def __repr__(self) -> str:
        return '\n'.join(self._repr())
    
    def set_texts(self, texts:List[str], update:bool=True):
        assert isinstance(texts, list), f''
        if self.is_single_instance:
            if len(texts) > 0:
                _text = str(texts[0])
                self.text = _text
                self.texts = [_text]
        else:
            box_count = len(self.boxes)
            # assert len(texts) == box_count, 'len of texts does not match len of self.boxes'
            _index_offset = 0
            for child in self:
                child_box_count = len(child.boxes)
                _texts = texts[_index_offset: _index_offset+child_box_count]
                child.set_texts(_texts, update=False)
                _index_offset += child_box_count
            
        if update:
            self.update_texts()
    
    def update_texts(self):
        if self.is_single_instance:
            self.texts = [self.text]
        else:
            self.texts = []
            for child in self:
                _texts = child.update_texts()
                self.texts.extend(_texts)
            self.text = ' '.join(self.texts)
        return self.texts
    
    @property
    def images(self):
        return [child.image for child in self]
    
    @property
    def text_all(self):
        if self.is_single_instance:
            return self.text
        return ' '.join([
            child.text_all if child.text_all else '<>'
            for child in self
        ])
    
    @property
    def df(self):
        if self.is_single_instance:
            data = [{
                'index': 0,
                'box': self.boxes[0],
                'text': self.text,
            }]
        else:
            data = [
                {
                    'index': i,
                    'box': _box,
                    'text': _text,
                }
                for i, (_box, _text) in enumerate(zip(self.boxes, self.texts))
            ]
        return pd.DataFrame(data, columns=['index', 'box', 'text'])
    
    @property
    def df_top(self):
        if self.is_single_instance:
            data = [{
                'index': 0,
                'box': self.boxes[0],
                'text': self.text,
            }]
        else:
            data = [
                {
                    'index': i,
                    'box': child.box_outer,
                    'text': child.text,
                }
                for i, child in enumerate(self)
            ]
        return pd.DataFrame(data, columns=['index', 'box', 'text'])
    
    def draw_anno(self,
                width=2,
                mode='box',
                draw_image=True,
                draw_level_0=False,
                img_base=None,
                draw_size=True,
                color=None,
                ):
        # DEPRECATED
        assert mode in ['box', 'mask', 'all']
        
        overlay_anno_bottom = AnnoDraw.draw_anno_box(
            self.size,
            boxes=self.boxes,
            color='#00FF00',
            color_text='#000000',
        )
        
        overlay_anno_top = AnnoDraw.draw_anno_box(
            self.size,
            boxes=self.boxes_top,
            color='#FF00FF',
            color_text='#000000',
        )
        overlay_anno = Image.alpha_composite(
            overlay_anno_bottom,
            overlay_anno_top,
        )
        img_anno = Image.alpha_composite(
            self.image.convert('RGBA'),
            overlay_anno,
        ).convert('RGB')
        
        return img_anno
    
    def to_grouped_imageboxes(self, **kwargs):
        '''group boxes with `grouped_boxes` from self and return an ImageBoxes with grouped boxes
        '''
        
        if len(self.boxes) > 0:
            boxes_grouped_final = self.group_boxes(self.boxes, **kwargs)
        else:
            boxes_grouped_final = np.array(self.boxes)
        
        imageboxes_grouped = ImageBoxes(
            boxes=boxes_grouped_final,
            image=self.image.copy(),
        )
        imageboxes_grouped.set_texts(self.texts)
        return imageboxes_grouped
    
    @classmethod
    def group_boxes(cls,
                boxes:Union[np.ndarray, list],
                
                merge_lines:bool=False,
                line_dist_max:float=1.0,
                line_dist_min:float=-0.1,
                line_iou_min:float=0.4,
                
                merge_rows:bool=True,
                row_hdist_max:float=0.4,
                row_vdist_max:float=1.8,
                row_height_ratio_min:float=0.8,
                
                merge_containing:bool=True,
                ) -> list:
        '''processes self.boxes and returns a new ImageBoxes object with grouped boxes
        Parameters:
            boxes
            merge_lines      (bool) False - whether to merge lines
            merge_rows       (bool) True - whether to merge rows
            merge_containing (bool) True - whether to merge overlaping boxes
            line_dist_max:          max distance between boxes to be in the same sentence (as a ratio of line height)
            line_dist_min:          min (negative) distance between boxes to be in the same sentence (as a ratio of line height)
            line_iou_min:           min vertical iou between boxes to be on the same line
            row_hdist_max:          max horizontal offset between rows to aligned as a column (as a ratio of line height)
            row_vdist_max:          max vertical distance between rows to be in the same column (as a ratio of line height)
            row_height_ratio_min:   min ratio between heights of rows to be in the same column
        Returns:
            boxes_nested_final (list): nested boxes
        '''
        _boxes = np.array(boxes)
        assert _boxes.ndim == 2
        assert _boxes.shape[-1] == 4
        
        merged_dfs = []
        merged_boxes = np.array(_boxes)
        
        if merge_lines:
            _df_merged = BoxMerge.group_texts_by_match_fn(
                merged_boxes,
                fn=BoxMerge.same_line_match,
                sort_index=0,
                dist_max=line_dist_max,
                dist_min=line_dist_min,
                iou_min=line_iou_min,
            )
            merged_dfs.append(_df_merged)
            merged_boxes = np.array(_df_merged['box'].tolist())
        
        if merge_rows:
            _df_merged = BoxMerge.group_texts_by_match_fn(
                merged_boxes,
                fn=BoxMerge.same_column_match,
                sort_index=1,
                hdist_max=row_hdist_max,
                vdist_max=row_vdist_max,
                height_ratio_min=row_height_ratio_min,
            )
            merged_dfs.append(_df_merged)
            merged_boxes = np.array(_df_merged['box'].tolist())
        
        if merge_containing:
            _df_merged = BoxMerge.group_texts_by_match_fn(
                merged_boxes,
                fn=BoxMerge.box_containing_match,
            )
            merged_dfs.append(_df_merged)
            merged_boxes = np.array(_df_merged['box'].tolist())
        
        indices_original = cls.get_original_nested_indices(merged_dfs)
        
        boxes_nested_final = [
            [
                _boxes[i].tolist()
                for i in _indices
            ]
            for _indices in indices_original
        ]
        return boxes_nested_final
    
    @classmethod
    def get_original_nested_indices(cls, df_groups: list) -> list:
        indices_nested = [
            [
                v.tolist()
                for v in _df['indices']
            ]
            for _df in df_groups
        ]
        
        indices_original = None
        for i, _indices in enumerate(indices_nested):
            if i == 0:
                indices_original = [list(v) for v in _indices]
            else:
                indices_original = [
                    [
                        v
                        for prev_index in prev_indices
                        for v in indices_original[prev_index]
                    ]
                    for prev_indices in _indices
                ]
        
        return indices_original

# %%