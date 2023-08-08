# %%
import numpy as np
import pandas as pd
from PIL import Image
from image2layout_computer_vision import (
    ImageBoxes,
    detect_text,
    detect_text_full,
    model_dispatch,
    AnnoDraw,
    ImageTransform,
)

# %%
img_fp = '/home/test/code/image2layout_computer_vision/data/inputs/Coterie benefits.png'
img_fp = '/home/test/code/image2layout_computer_vision/data/inputs/Screenshot 2023-07-13 at 11.03.48.png'
img = Image.open(img_fp).convert('RGB')
# img

# %%
data_merged, data_raw = detect_text_full(
    img,
#     row_hdist_max=0.6,
#     row_vdist_max=1.4,
#     row_height_ratio_min=0.8,
)
data_merged, data_raw

img_anno_merged = AnnoDraw.draw_anno_text_overlay(
    img=img,
    boxes=[v['box'] for v in data_merged],
    texts=[v['text'] for v in data_merged],
    width=2,
    text_pad=None,
    # color='#00FF88',
    color_text='#000000',
    # font=None,
    # font='data/OpenSans_Condensed-Medium.ttf',
    opacity=0.75,
)

img_anno_raw = AnnoDraw.draw_anno_text_overlay(
    img=img,
    boxes=[v['box'] for v in data_raw],
    texts=[v['text'] for v in data_raw],
    width=2,
    text_pad=None,
    # color='#00FF88',
    color_text='#000000',
    # font='OpenSans_Condensed-Medium.ttf',
    # font='data/OpenSans_Condensed-Medium.ttf',
    opacity=0.75,
)

img_anno_merged.convert('RGB')

# %%
img_anno_dual = ImageTransform.concatenate(
    [img_anno_merged],
    # [img_anno_merged, img_anno_raw],
    # [img, img_anno_merged],
    # [img, img_anno_raw, img_anno_merged],
    columns=1,
    spacing=10,
)
img_anno_dual.convert('RGB')

# %%





# %%