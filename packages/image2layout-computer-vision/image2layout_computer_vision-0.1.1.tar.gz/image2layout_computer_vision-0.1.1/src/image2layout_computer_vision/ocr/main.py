# %%
import time
import json
import os
import numpy as np
import pandas as pd
from PIL import Image
from typing import Union, Any, List, Dict, Tuple
from ..utils import get_image, ImageConvert
from .imagebox import ImageBoxes, BoxMerge

# %%
import logging
debug_logger = logging.getLogger('ocr')
c_handler = logging.StreamHandler()
debug_logger.addHandler(c_handler)
debug_logger.setLevel(logging.WARNING)

# %%
# from .model_layoutmlv2 import ModelDispatch_LayoutMLv2
# model_dispatch_layout = ModelDispatch_LayoutMLv2(
#     device='cpu',
# )

# %%
from .model_paddle import ModelDispatch_Paddle
model_dispatch_paddle = ModelDispatch_Paddle(
    device='cpu',
)

# %%
model_dispatch = model_dispatch_paddle

# %%
def detect_text(image: Union[Image.Image, np.ndarray], merge_boxes=True, **kwargs) -> ImageBoxes:
    '''predict boxes for text in the image
    Parameters:
        image: (PIL.Image.Image, np.ndarray) RGB image
        **kwargs:
            line_dist_max:          max distance between boxes to be in the same sentence (as a ratio of line height)
            line_dist_min:          min (negative) distance between boxes to be in the same sentence (as a ratio of line height)
            line_iou_min:           min vertical iou between boxes to be on the same line
            row_hdist_max:          max horizontal offset between rows to aligned as a column (as a ratio of line height)
            row_vdist_max:          max vertical distance between rows to be in the same column (as a ratio of line height)
            row_height_ratio_min:   min ratio between heights of rows to be in the same column
    Returns:
        imageboxes: (ImageBoxes) object containing prediction boxes
    '''
    _image = get_image(image).convert('RGB')
    debug_logger.debug(msg=f'detect_text | input[{_image.size}]')
    
    result_df = model_dispatch_paddle(_image)
    
    imageboxes_raw = ImageBoxes(
        image=_image,
        boxes=result_df['box'].tolist(),
    )
    if merge_boxes:
        imageboxes = imageboxes_raw.to_grouped_imageboxes(**kwargs)
        debug_logger.debug(msg=f'detect_text | merged[{len(imageboxes_raw.boxes_top)} -> {len(imageboxes.boxes_top)}]')
        return imageboxes
    
    return imageboxes_raw

# %%
def detect_text_boxes(image: Union[Image.Image, np.ndarray], **kwargs) -> Tuple[np.ndarray, np.ndarray]:
    '''predict boxes for text in the image
    Parameters: (same as detect_text)
    Returns:
        boxes_merged: (np.ndarray) [M, 4] text boxes detected, merged boxes
        boxes_raw:    (np.ndarray) [N, 4] text boxes detected, all individual boxes (N >= M)
    '''
    imageboxes = detect_text(image, **kwargs)
    
    boxes_merged = np.array(imageboxes.boxes_top, int)
    boxes_raw = np.array(imageboxes.boxes, int)
    return boxes_merged, boxes_raw

# %%
def detect_text_full(image: Union[Image.Image, np.ndarray], **kwargs) -> List[Dict]:
    _image = get_image(image).convert('RGB')
    result_df = model_dispatch_paddle(image)
    result_data = result_df.to_dict('records')
    imageboxes_raw = ImageBoxes(
        image=_image,
        boxes=result_df['box'].tolist(),
    )
    imageboxes_raw.set_texts(result_df['text'].tolist())
    imageboxes_merged = imageboxes_raw.to_grouped_imageboxes(**kwargs)
    
    return imageboxes_merged.df_top.to_dict('records'), imageboxes_raw.df_top.to_dict('records')

# %%
if __name__ == '__main__':
    imageboxes = detect_text('data/inputs/SCR-20230710-ixfw.jpeg')
    
    imageboxes.draw_anno(width=3)
    
    boxes_merged = np.array(imageboxes.boxes_top, int)
    boxes_raw = np.array(imageboxes.boxes, int)
