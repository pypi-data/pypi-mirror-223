# %%
import os
import glob
import json
import numpy as np
import pandas as pd
import enlighten
from PIL import Image

from image2layout_computer_vision import (
    extract_colors, ColorExtractor, COLOR, ImageTransform,
    get_image, PixelMask
)

# %%
image_dp = '../data/inputs'
image_fps = glob.glob(os.path.join(image_dp, '*.png'))
image_fps

# %%
# image_fps = image_fps[:2]
data = []
pbar = enlighten.Counter(total=len(image_fps))
for fp in image_fps:
    img = Image.open(fp).convert('RGB')
    CE = ColorExtractor(img)
    CE.colors
    data.append({
        'path': fp,
        'size': img.size,
        'color_bg': CE.color_bg,
        'color_fg': CE.color_fg,
    })
    pbar.update()

data

# %%
with open('../data/reference_color_extracted.json', 'w') as fo:
    json.dump(data, fo, indent=4)

# %%
