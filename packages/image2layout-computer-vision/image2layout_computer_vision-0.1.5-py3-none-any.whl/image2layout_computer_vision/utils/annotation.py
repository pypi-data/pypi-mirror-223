# %%
import os, time, string, json
import numpy as np
import pandas as pd
import colorsys
from PIL import Image, ImageFont, ImageDraw
from typing import Union, Any, List, Dict, Tuple
from .color_system import COLOR
from .imaging import get_image, ImageConvert, ImageTransform

# %%
FONT_PATH = os.path.join(os.path.split(__file__)[0], 'OpenSans_Condensed-Medium.ttf')

# %%
class AnnoDraw:
    
    @classmethod
    def draw_anno_box(cls,
                img=(10, 10),
                boxes:Union[np.ndarray, list]=[],
                texts=None,
                width=None,
                text_pad=None,
                color='#00FF00',
                color_text='#000000',
                font=FONT_PATH,
                opacity=1.0,
                ):
        
        if isinstance(img, (tuple, list)):
            size = tuple(img)
        else:
            size = img.size
        
        img_anno = Image.new('RGBA', size)
        
        size_min = (min(size) + np.linalg.norm(size)) / 2
        if isinstance(font, str) and os.path.isfile(font):
            font = ImageFont.truetype(font, int(size_min // 60))
        else:
            font = ImageFont.load_default()
        
        width = int(max(size_min // 600 if width is None else width, 1))
        text_pad = int(max(size_min // 400 if text_pad is None else text_pad, 1))
        
        draw = ImageDraw.Draw(img_anno)
        drawing_texts = isinstance(texts, list) and len(texts) == len(boxes)
        for i, box in enumerate(boxes):
            _box = np.array(box)
            draw.rectangle(
                tuple(_box),
                outline=color,
                width=width,
            )
            
            if drawing_texts:
                _size = _box[2:] - _box[:2]
                # _text = f'{_size[0]}•{_size[1]}'
                _text = texts[i]
                _text_box = np.array(font.getbbox(_text))
                _text_size = _text_box[2:] - _text_box[:2] + [text_pad * 2] * 2
                _text_box_padded = np.tile(_text_size, 2) * [-.5, -1, .5, 0]
                _text_offset = _text_box_padded[:2] + [text_pad, 0]
                _anchor = [(_box[0] + _box[2]) / 2, _box[1]]
                
                draw.rectangle(
                    tuple(_text_box_padded + np.tile(_anchor, 2)),
                    fill=color,
                )
                draw.text(
                    tuple(_text_offset + _anchor),
                    text=_text,
                    fill=color_text,
                    font=font,
                )
        
        if isinstance(img, Image.Image):
            if opacity < 1:
                assert opacity > 0, f'opacity[{opacity}]'
                img_anno.putalpha(img_anno.getchannel('A').point(lambda x: x * opacity))
            
            img_anno = Image.alpha_composite(
                img.convert('RGBA'),
                img_anno,
            )
        return img_anno
    
    
    STRING_CHARS = string.ascii_letters + string.digits
    @classmethod
    def draw_text_center(cls,
                draw,
                text,
                font,
                pos=(0, 0),
                color_text=(0, 0, 0),
                color_bg=None,
                ):
        
        try:
            ascent, descent = font.getmetrics()
            (width, baseline), (offset_x, offset_y) = font.font.getsize(cls.STRING_CHARS)
            
            text_ys = np.cumsum([0, offset_y, ascent - offset_y, descent])
            
            (text_width, _), (_, _) = font.font.getsize(text)
        except Exception as e:
            text_ys = np.cumsum([0, 3, 5, 3])
            text_width = font.getbbox(text)[2]
            descent = 3
        
        _pos = np.array(pos)
        
        text_box = np.array([
            0, text_ys[1],
            text_width, text_ys[3],
        ])
        text_size = text_box[2:] - text_box[:2]
        text_offset = - (text_size / 2 + [0, text_ys[1] * 0.6])
        text_box_ex = text_box + np.repeat([-1, 1], 2) * 3 + np.array([-1, -1/2, 1, 0]) * descent
        # text_box_ex = text_box + np.repeat([-1, 1], 2) * 3 + np.array([-1, -1, 1, 0]) * descent
        
        if color_bg is not None:
            draw.rectangle(
                tuple(np.tile(_pos + text_offset, 2) + text_box_ex),
                fill=color_bg,
            )
        draw.text(
            tuple(_pos + text_offset + [0, 0]),
            text=text,
            fill=color_text,
            font=font,
        )
        return draw
    

    @classmethod
    def draw_anno_text_overlay(cls,
                img:tuple=(10, 10),
                boxes:list=[],
                texts:list=None,
                width:int=None,
                text_pad:int=None,
                color:string=None,
                color_text:string='#000000',
                bg_saturation:float=0.8,
                bg_value:float=0.8,
                font:str=FONT_PATH,
                opacity:float=0.65,
                ):
        
        if isinstance(img, (tuple, list)):
            size = tuple(img)
        else:
            img = get_image(img).convert('RGBA')
            size = img.size
        
        img_box = Image.new('RGBA', size)
        img_text = Image.new('RGBA', size)
        
        size_min = (min(size) + np.linalg.norm(size)) / 2
        
        is_loading_font_from_file = isinstance(font, str) and os.path.isfile(font)
        # assert is_loading_font_from_file, f'cwd[{os.getcwd()}] font[{font}] __file__[{__file__}]'
        _font = None
        if not is_loading_font_from_file:
            _font = ImageFont.load_default()
        
        if width is True:
            width = int(max(size_min // 600, 1))
        assert width is None or isinstance(width, int)
        text_pad = int(max(size_min // 400 if text_pad is None else text_pad, 1))
        
        draw_box = ImageDraw.Draw(img_box)
        draw_text = ImageDraw.Draw(img_text)
        drawing_texts = isinstance(texts, list) and len(texts) == len(boxes)
        
        for i, box in enumerate(boxes):
            _box = np.array(box)
            _box_size = _box[2:] - _box[:2]
            _box_xy_center = (_box[:2] + _box[2:]) / 2
            
            _color = color if color is not None else tuple([int(v * 255) for v in colorsys.hsv_to_rgb(
                i * max(1 / len(boxes), 1/12),
                bg_saturation,
                bg_value,
            )])
            
            draw_box.rectangle(
                tuple(_box),
                fill=_color,
            )
            if width is not None:
                draw_box.rectangle(
                    tuple(_box),
                    outline=color_text,
                    width=width,
                )
            
            if drawing_texts:
                _text = texts[i]
                _text_size = np.min(_box_size * [2.5 / len(_text), 1.1])
                
                if is_loading_font_from_file:
                    _font_size = int(max(np.floor(_text_size), 8))
                    _font = ImageFont.truetype(font, size=_font_size)
                
                cls.draw_text_center(
                    draw_text,
                    _text,
                    font=_font,
                    pos=tuple(_box_xy_center),
                    color_text=color_text,
                )
        
        if opacity != 1:
            img_box = ImageTransform.setalpha(img_box, scale=opacity)
        
        if isinstance(img, Image.Image):
            img_anno = ImageTransform.composite(img, img_box, img_text)
        else:
            img_anno = ImageTransform.composite(img_box, img_text)
        
        return img_anno
    
    