# %%
import os
import time
import numpy as np
import pandas as pd
from datasets import load_dataset
from PIL import Image, ImageDraw, ImageFont

from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification

# %%
# disable LayoutLMv2 tokenizers warning
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# %%
class ModelDispatch_Image:
    def __init__(self,
                model_pipeline,
                model_name,
                processor_pipeline=None,
                processor_name=None,
                device='cpu',
                auto_load=False,
                log_telemetry=False,
                **kwargs
                ):
        self.processor = None
        self.model = None
        self.device = device
        self.model_pipeline = model_pipeline
        self.model_name = model_name
        self.processor_pipeline = processor_pipeline
        self.processor_name = processor_name
        self.loaded = False
        self.log_telemetry = bool(log_telemetry)
        self.telemetry = {
            'load_time': None,
            'forward_time': [],
        }
        if auto_load:
            self._load()
    
    def __repr__(self) -> str:
        loaded_str = '' if self.loaded else ' (not_loaded)'
        return f'{self.__class__.__name__}[{self.model_name}](device[{self.device}]){loaded_str}'
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
    
    def _load(self,):
        time_start = time.perf_counter()
        assert self.model_pipeline is not None
        assert self.model_name is not None
        self.model = self.model_pipeline.from_pretrained(self._model_name)
        self.model.to(self.device)
        if self.processor_pipeline is not None:
            if self.processor_name is not None:
                self.processor = self.processor_pipeline.from_pretrained(self.processor_name)
        self.loaded = True
        if self.log_telemetry:
            time_elapsed = time.perf_counter() - time_start
            self.telemetry['load_time'] = time_elapsed
        
    
    def _forward(self, *args, **kwargs):
        '''logic for forward pass, implement in child classes
        '''
        raise NotImplementedError()
    
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


class ModelDispatch_LayoutMLv2(ModelDispatch_Image):
    labels = ['O', 'B-HEADER', 'I-HEADER', 'B-QUESTION', 'I-QUESTION', 'B-ANSWER', 'I-ANSWER']
    id2label = {v: k for v, k in enumerate(labels)}
    label2color = {'question':'blue', 'answer':'green', 'header':'orange', 'other':'violet'}
    model_names = [
        'nielsr/layoutlmv2-finetuned-funsd',
    ]
    
    def __init__(self, model_name='nielsr/layoutlmv2-finetuned-funsd', **kwargs):
        assert model_name in self.model_names, f'`model_name` must be one of {self.model_names}, found {model_name}'
        super().__init__(
            model_pipeline=LayoutLMv2ForTokenClassification,
            model_name=model_name,
            processor_pipeline=LayoutLMv2Processor,
            processor_name='jinhybr/OCR-LM-v1',
            **kwargs
        )
    
    def _load(self):
        self.processor = LayoutLMv2Processor.from_pretrained(self.processor_name)
        self.model = LayoutLMv2ForTokenClassification.from_pretrained(self.model_name)
        self.model.to(self.device)
        self.loaded = True
    
    def _unload(self):
        del self.model
        self.model = None
        self.loaded = False
    
    def _forward(self, image):
        width, height = image.size

        # encode
        encoding = self.processor(image, truncation=True, return_offsets_mapping=True, return_tensors="pt")
        offset_mapping = encoding.pop('offset_mapping')

        # forward pass
        feed = {k: v.to(self.device) for k, v in encoding.items()}
        outputs = self.model(**feed)

        # get predictions
        predictions = outputs.logits.argmax(-1).squeeze().tolist()
        token_boxes = encoding.bbox.squeeze().tolist()

        # only keep non-subword predictions
        is_subword = np.array(offset_mapping.squeeze().tolist())[:,0] != 0
        true_predictions = [self.id2label[pred] for idx, pred in enumerate(predictions) if not is_subword[idx]]
        true_boxes = [self.unnormalize_box(box, width, height) for idx, box in enumerate(token_boxes) if not is_subword[idx]]
        
        return true_predictions, true_boxes
    
    @classmethod
    def unnormalize_box(cls, bbox, width, height):
        return [
            width * (bbox[0] / 1000),
            height * (bbox[1] / 1000),
            width * (bbox[2] / 1000),
            height * (bbox[3] / 1000),
        ]
    
    @classmethod
    def iob_to_label(cls, label):
        label = label[2:]
        if not label:
            return 'other'
        return label
    
    def draw_preds(self, image, true_predictions, true_boxes):
        _image = image.copy()
        draw = ImageDraw.Draw(_image)
        font = ImageFont.load_default()
        for prediction, box in zip(true_predictions, true_boxes):
            predicted_label = self.iob_to_label(prediction).lower()
            draw.rectangle(box, outline=self.label2color[predicted_label])
            draw.text((box[0]+10, box[1]-10), text=predicted_label, fill=self.label2color[predicted_label], font=font)
        return _image

# %%
if __name__ == '__main__':
    model_dispatch = ModelDispatch_LayoutMLv2(
        device='cpu',
    )
    image = Image.open('data/inputs/image 559.png').convert('RGB')
    true_predictions, true_boxes = model_dispatch(image)
    
    image_anno = model_dispatch.draw_preds(
        image,
        true_predictions, true_boxes
    )
    os.makedirs('data', exist_ok=True)
    image_anno.save('data/anno.png')
    
    print('model ocr ran successfully')
