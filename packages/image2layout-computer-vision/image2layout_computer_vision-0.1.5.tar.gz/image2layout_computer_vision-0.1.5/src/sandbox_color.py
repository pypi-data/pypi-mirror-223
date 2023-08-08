# %%
import os, time, string, json
import glob
import numpy as np
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = 'plotly_dark'
from typing import Union, Any, List, Dict, Tuple
from enlighten import Counter

# %%
from image2layout_computer_vision import (
    extract_colors, ColorExtractor, COLOR, ImageTransform,
    get_image, PixelMask
)

# %%
limit = 40
image_dp = '/home/test/code/image2layout_computer_vision/data/url'

# %%
image_urls = [
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureanuasmdpml.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureoqcwigcwqa.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureyobfdvzfie.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureoxhsyxmqpl.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezfemgoqvtj.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturebwifmzvsjp.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturelczqrwikus.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureqbxksbkbdt.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezikiawqlqa.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureeaulvtzdgt.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureprdtrapfdz.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturegbwsxoaktj.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexcohyovdee.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureimedbfqkrf.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexyiopumpxj.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturegjxeswtrmm.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturehwwmldjjtm.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturegpsetrmvog.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureyrlfgkxkll.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturergremmpbsw.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureaxeyylmgus.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturettdzbzorfe.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezzmiwmfpyx.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezyqgbuqbwk.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturehbhmuahugj.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturewkhzhwnaye.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureqjcjwjshbm.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturetafeshntjx.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureotxringwso.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturefnmhzplqpb.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexoaircxhqv.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureejkupjvwyl.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturekpxovjdcem.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezdyujccirt.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturewqllcrrlgd.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureeuwlxaoafb.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturejwfgwazzhx.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturenifptdacsx.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturentwfjfqypi.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturecisfcuzmpu.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturetigcomxqsv.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturemsddyauvlh.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezmdmvlrqzc.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureucqhvmnhsk.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturerlbapnzaal.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexxruwczzvz.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturedvqcfcjvwd.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureoscxxvmtuy.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturesbykccypup.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturepugcqgdthj.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturewtdxuckevt.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturejlmzwzxdks.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureqhitnykrrj.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturetsgxrruxcj.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezeewakfjdp.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureieunnhxiol.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturemlxqoxijoc.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturelwagfgbeci.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureguzpvcswjo.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezzntvzizhz.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureayvhbhddnp.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturevdmpghvhxt.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturegldtqhxtzv.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturevqonpbsbhz.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturejyhjhqsxon.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturerkgdhzlsug.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureahdlhrzksx.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturekfcdyzhylg.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturesbozzutkwq.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturehfegmpknpp.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturefcanbgatus.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturebrwupcbibz.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureirfgdpghxo.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturehutlrclzwe.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureueuqlzbuog.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexrybhjwuzs.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturebpcmgxckzs.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureouvhhsqner.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureangzfopmsh.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturezhwrmdzjbf.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureqmbadiscdv.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturepcdanmnnsk.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexzkktdxuyb.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturejupwjtuvlc.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturerhntdwwxdc.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturefslqajigey.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexwkuzzqxjk.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturerravqbrwxc.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturequpuywtckh.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturedyabtzdzqt.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureochgrugsxm.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexeolgdtukc.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureznwzjazlfb.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureahdpwpygrh.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturebnpzztelbs.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturejqpvwfclip.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturehhkpnxtrbv.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturexutujxskuq.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_captureuzvizuapuc.png',
    'https://gemai-dev.s3.amazonaws.com/image2layout/section_capturelaguhcaebj.png',
]

# fps = np.random.choice(image_urls, limit, replace=False).tolist()
# len(fps)

# pbar = Counter(total=len(image_urls))
# os.makedirs(image_dp, exist_ok=True)
# for i, url in enumerate(image_urls):
#     _img = get_image(url).convert('RGB')
#     _filename = url.split('/')[-1].lower()
#     if not _filename.endswith('.png'):
#         _filename = f'{_filename}.png'
#     _fp = os.path.join(image_dp, _filename)
#     _img.save(_fp, 'PNG')
#     del _img
#     pbar.update()

# import sys
# sys.exit()
# %%
# fps = [
#     '/Users/felixdo/Documents/Code/AI/image2layout-computer-vision/data/inputs/section_capturenmvqljbvbg.png',
#     '/Users/felixdo/Documents/Code/AI/image2layout-computer-vision/data/inputs/section_capturezxspaifrgr.png',
# ]

fps = glob.glob(os.path.join(image_dp, '*.png'))
fps = np.random.choice(fps, limit, replace=False).tolist()
len(fps)

# # %%
# data = []
# color_extractors = []

# pbar = Counter(total=len(fps))

# for i, fp in enumerate(fps):
#     _img = get_image(fp).convert('RGB')
#     n_pixels = int(np.prod(_img.size))
    
#     time_start = time.perf_counter()
    
#     _ce = ColorExtractor(_img)
#     color_extractors.append(_ce)
    
#     time_cost = time.perf_counter() - time_start
    
#     data.append({
#         'size': _img.size,
#         'n_pixels': n_pixels,
#         'time_cost': time_cost,
#         'color_bg': _ce.color_bg,
#         'color_fg': _ce.color_fg,
#     })
#     del _img
#     pbar.update()

# color_extractors
# df = pd.DataFrame(data)
# df

# # %%
# fig = px.scatter(
#     df,
#     x='n_pixels',
#     y='time_cost',
# )
# fig.write_image('../data/color_extract_speed.png')

# %%







# %%
img = Image.open(fps[0]).convert('RGB')
img

# %%
# sorted(img.getcolors(np.prod(img.size)))[-5:][::-1]

# # %%
# coord = PixelMask.coordinates(img.size[::-1])
# coord_cell = np.floor(coord / 40).astype(int)
# coord_mod = coord_cell % 2
# coord_checker = coord_mod[:, :, 0] == coord_mod[:, :, 1]
# coord_checker

# # %%
# px.imshow(coord_checker)

# %%
img

# %%
CE = ColorExtractor(img)
CE
print('done')
print(CE)

# %%
# CE.draw_anno()

# %%