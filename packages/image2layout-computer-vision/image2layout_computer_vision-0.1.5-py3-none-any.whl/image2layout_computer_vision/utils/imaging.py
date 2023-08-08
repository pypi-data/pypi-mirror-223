# %%
import os
import numpy as np
from PIL import Image, ImageDraw

import requests
import base64
from io import BytesIO

from typing import Union, Callable, Any, Dict, List, Tuple

# %%
class ImageConvert:
    @classmethod
    def pil2bytes(cls, image, format='PNG') -> str:
        buffered = BytesIO()
        image.save(buffered, format=format)
        img_bytes = base64.b64encode(buffered.getvalue())
        return img_bytes
    
    @classmethod
    def bytes2pil(cls, img_bytes, decode=True):
        _img_bytes = base64.b64decode(img_bytes) if decode else img_bytes
        bytesio = BytesIO(_img_bytes)
        bytesio.seek(0)
        return Image.open(bytesio)
    
    @classmethod
    def pil2str(cls, image, format='PNG') -> str:
        return cls.pil2bytes(image=image, format=format).decode('utf-8')
    
    @classmethod
    def str2pil(cls, img_str: str):
        if img_str.startswith('data:image/'):
            comma_index = img_str.find(',')
            if comma_index >= 0:
                img_str = img_str[comma_index + 1:].strip()
        return cls.bytes2pil(img_bytes=img_str.encode('utf-8'))

# %%
def get_image(image):
    if isinstance(image, Image.Image):
        return image
    if isinstance(image, str):
        if os.path.isfile(image):
            return Image.open(image)
        else:
            res = requests.get(image)
            if res.status_code == 200:
                return ImageConvert.bytes2pil(res.content, decode=False)
        raise ValueError('`image` of type <str> is not a valid filepath or url')
    if isinstance(image, bytes):
        return ImageConvert.bytes2pil(image)
    if isinstance(image, np.ndarray):
        return Image.fromarray(image)
    raise ValueError(f'`image` of type {type(image)} is not supported.')

# %%
class ImageTransform:
    # TODO: implement and separate different types of concatenation
    @classmethod
    def concatenate(cls, images: list, columns:int=0, resize='original', spacing=10):
        '''concatenate images horizontally, and onto multiple rows if columns is specified
        '''
        assert resize in ['fill', 'fit', 'original'], f''
        
        # TODO: supports other resizing methods
        assert resize in ['original'], f'currently only supports resize=original'
        
        _imgs = [get_image(_img) for _img in images]
        count = len(_imgs)
        assert count >= 2
        sizes = np.array([_img.size for _img in _imgs])
        max_size = np.max(sizes, axis=0)
        
        if columns is None or columns < 1:
            # same row for all images
            cell_width, cell_height = max_size
            
            total_size = np.array([
                sizes[:, 0].sum() + spacing * (count - 1),
                cell_height,
            ]).astype(int)
            img_out = Image.new('RGBA', tuple(total_size))
            
            for index in range(count):
                cell_offset_x = sizes[:index, 0].sum() + spacing * index
                offset_x = int((cell_width - sizes[index, 0]) // 2) + cell_offset_x
                offset_y = int((cell_height - sizes[index, 1]) // 2)
                
                img_out.paste(_imgs[index], (offset_x, offset_y))
        else:
            assert isinstance(columns, int)
            rows = int(np.ceil(count / columns))
            total_size = max_size * [columns, rows] + spacing * (np.array([columns, rows]) - 1)
            img_out = Image.new('RGBA', tuple(total_size))
            
            for cell_y in range(rows):
                for cell_x in range(columns):
                    index = columns * cell_y + cell_x
                    if index >= count:
                        break
                    cell_offset = (max_size + spacing) * [cell_x, cell_y]
                    img_offset = (max_size - sizes[index]) // 2
                    img_pos = cell_offset + img_offset
                    img_out.paste(_imgs[index], tuple(img_pos))
                
            
        return img_out
    
    @classmethod
    def setalpha(cls,
                image: Image.Image,
                scale: Union[float, None]=None,
                alpha: Union[Callable, float, int, None]=None,
                mask: Union[Image.Image, np.ndarray]=None,
                ):
        '''
        scale: (optional)
            (float) value to multiply alpha with
        alpha: (optional)
            (float, int) alpha value to set
            (Callable) fn to apply to alpha channel
        mask: (optional)
            (Image.Image) the Image to set as alpha
            (np.ndarray) the single channel numpy array to set as alpha
        '''
        img = image.convert('RGBA')
        
        if alpha is not None:
            assert scale is None, f'set only one of [scale, alpha, mask]'
            assert mask is None, f'set only one of [scale, alpha, mask]'
            if callable(alpha):
                _fn = alpha
            else:
                _alpha = int(min(max(alpha, 0), 255))
                _fn = lambda x: _alpha
            img.putalpha(img.getchannel('A').point(_fn))
            
        elif scale is not None:
            assert mask is None, f'set only one of [scale, alpha, mask]'
            _fn = lambda x: int(min(max(x * scale, 0), 255))
            img.putalpha(img.getchannel('A').point(_fn))
            
        elif mask is not None:
            if isinstance(mask, np.ndarray):
                if mask.dtype == np.bool_:
                    _mask = mask * 255
                else:
                    _mask = mask.astype(int)
                img_mask = Image.fromarray(
                    np.clip(_mask, 0, 255).astype(np.uint8),
                    'L',
                )
            else:
                assert isinstance(mask, Image.Image)
                try:
                    # extract A channel
                    img_mask = mask.getchannel('A')
                except ValueError as e:
                    pass
                finally:
                    img_mask = mask.convert('L')
                
            img.putalpha(img_mask)
        
        return img
    
    @classmethod
    def composite(cls, *images: Image.Image):
        count = len(images)
        if count == 0:
            return None
        if count == 1:
            return images[0]
        
        img_out = images[0].convert('RGBA')
        for i in range(1, count):
            img_next = images[i].convert('RGBA')
            img_out = Image.alpha_composite(
                img_out,
                img_next,
            )
        return img_out
        

# %%
