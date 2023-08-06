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
)

# %%
img = Image.open('/home/test/code/image2layout_computer_vision/data/inputs/Coterie benefits.png').convert('RGB')
img

# %%
data_merged, data_raw = detect_text_full(img)
data_merged, data_raw

# %%
AnnoDraw.draw_anno_text_overlay(
    img=img,
    boxes=[v['box'] for v in data_merged],
    texts=[v['text'] for v in data_merged],
    width=2,
    text_pad=None,
    # color='#00FF88',
    color_text='#000000',
    # font='data/OpenSans_Condensed-Medium.ttf',
    opacity=0.75,
).convert('RGB')

# %%
AnnoDraw.draw_anno_text_overlay(
    img=img,
    boxes=[v['box'] for v in data_raw],
    texts=[v['text'] for v in data_raw],
    width=2,
    text_pad=None,
    # color='#00FF88',
    color_text='#000000',
    # font='data/OpenSans_Condensed-Medium.ttf',
    opacity=0.75,
).convert('RGB')

# %%





# %%
df = model_dispatch(img)
df

# %%
imageboxes = detect_text(img)
imageboxes

# %%
imageboxes.set_texts(df['text'].tolist())
imageboxes

# %%
imageboxes.df

# %%
IB = ImageBoxes(
    image=img,
    boxes=imageboxes.boxes_top,
)

# %%