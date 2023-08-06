# %%
from paddleocr import PaddleOCR, draw_ocr
import time, os
import numpy as np
import pandas as pd
import string
import colorsys
from PIL import Image, ImageDraw, ImageFont

from ..utils import draw_anno_text_overlay

# %%
class ModelDispatch_Paddle:
    def __init__(self,
                device='cpu',
                auto_load=False,
                log_telemetry=False,
                ):
        assert device in ['cpu', 'cuda']
        self.device = device
        self.paddle_ocr = None
        self.loaded = False
        self.log_telemetry = bool(log_telemetry)
        self.telemetry = {
            'load_time': None,
            'forward_time': [],
        }
        if auto_load:
            self._load()
    
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
    
    def _load(self):
        self.paddle_ocr = PaddleOCR(
            lang='en',
            use_gpu=self.device in ['cuda'],
            use_angle_cls=True,
        )
        self.loaded = True
    
    def _unload(self):
        del self.paddle_ocr
        self.paddle_ocr = None
        self.loaded = False
    
    def forward(self, *args, **kwargs):
        '''default wrapper for _forward method
        '''
        if not self.loaded:
            self._load()
        
        time_start = time.perf_counter()
        
        _output = self._forward(*args, **kwargs)
        
        if self.log_telemetry:
            time_elapsed = time.perf_counter() - time_start
            self.telemetry['forward_time'].append(time_elapsed)
            self.telemetry['forward_time'] = self.telemetry['forward_time'][-20:]
        
        return _output
    
    def _forward(self, image:Image.Image) -> pd.DataFrame:
        width, height = image.size
        
        result = self.paddle_ocr.ocr(np.array(image.convert('RGB')), cls=True)
        
        result_df = pd.DataFrame([
            {
                'text': d[1][0],
                'score': d[1][1],
                'box': [int(v) for v in [*d[0][0], *d[0][2]]],
            }
            for res in result
            for d in res
        ])
        return result_df

# %%