# %%
import os
import numpy as np
from PIL import Image, ImageDraw

import requests
import base64
from io import BytesIO

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
    @classmethod
    def concatenate(cls, imgs: list, columns:int=0, resize='original', spacing=10):
        '''concatenate images horizontally, and onto multiple rows if columns is specified
        '''
        assert resize in ['fill', 'fit', 'original'], f''
        
        # TODO: supports other resizing
        assert resize in ['original'], f'currently only supports resize=original'
        
        count = len(imgs)
        _imgs = [get_image(_img) for _img in imgs]
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
            total_size = max_size * [columns, rows]
            img_out = Image.new('RGBA', tuple(total_size))
            
            for cell_y in range(rows):
                for cell_x in range(columns):
                    index = columns * cell_y + cell_x
                    if index >= count:
                        break
                    cell_offset = max_size * [cell_x, cell_y]
                    img_offset = (max_size - sizes[index]) // 2
                    img_pos = cell_offset + img_offset
                    img_out.paste(_imgs[index], tuple(img_pos))
                
            
        return img_out


# %%
