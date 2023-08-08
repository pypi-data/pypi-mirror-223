# %%
import time, os
import glob
import numpy as np
import pandas as pd
from PIL import Image
from image2layout_computer_vision import (
    ImageBoxes,
    detect_text,
    detect_text_full,
    detect_text_boxes,
    detect_text_element,
    detect_text_elements,
    model_dispatch,
    AnnoDraw,
    ImageTransform,
    COLOR,
    # RecognitionAndDetection,
    Chrono,
)
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = 'plotly_dark'


# %%
img_fp = '/home/test/code/image2layout_computer_vision/data/inputs/Coterie benefits.png'
img_fp = '/home/test/code/image2layout_computer_vision/data/inputs/Screenshot 2023-07-13 at 11.03.48.png'
img = Image.open(img_fp).convert('RGB')
image_np = np.array(img)
img.size
# img

# %%
data_merged, data_raw = detect_text_full(
    img,
    # row_hdist_max=0.6,
    # row_vdist_max=1.4,
    # row_height_ratio_min=0.8,
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
data_merged, data_raw = RecognitionAndDetection.detect_text_boxes(
    img,
)
img_anno_boxes = AnnoDraw.draw_anno_text_overlay(
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
img_anno_boxes.convert('RGB')

# %%
data_raw = RecognitionAndDetection.detect_text_element(
    img,
)

img_anno_element = AnnoDraw.draw_anno_text_overlay(
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
img_anno_element.convert('RGB')


# %%
# results = model_dispatch.paddle_ocr.ocr(image_np, cls=True)
results = model_dispatch.paddle_ocr.ocr(image_np, rec=False)
# results = model_dispatch.paddle_detect.ocr(image_np, rec=False)
results

# %%
fps = glob.glob('/home/test/code/image2layout_computer_vision/data/inputs/*.png')[:3]
data = []
for i, fp in enumerate(fps):
    _img = Image.open(fp).convert('RGB')
    
    for j in list(range(2)):
        detection_only = (i % 2 == j)
        time_start = time.perf_counter()
        if detection_only:
            data_merged, data_raw = RecognitionAndDetection.detect_text_boxes(
                _img,
            )
        else:
            data_raw = RecognitionAndDetection.detect_text_element(
                _img,
            )
        time_cost = time.perf_counter() - time_start
        data.append({
            'image_index': i,
            'detection_only': detection_only,
            'time_cost': time_cost,
        })
    
    print(f'\r[{i+1}/{len(fps)}]      ', end='')

df = pd.DataFrame(data)
df

# %%
px.scatter(
    df,
    x='image_index',
    y='time_cost',
    color='detection_only',
)