from . import ocr, color_extract, utils

from .ocr import ImageBoxes, BoxMerge, model_dispatch, RecognitionAndDetection
from .color_extract import ColorExtractor, extract_colors
from .utils import get_image, ImageConvert, COLOR, PixelMask, ImageTransform, Chrono, Timer, AnnoDraw

detect_text = RecognitionAndDetection.detect_text
detect_text_full = RecognitionAndDetection.detect_text_full
detect_text_boxes = RecognitionAndDetection.detect_text_boxes
detect_text_element = RecognitionAndDetection.detect_text_element
detect_text_elements = RecognitionAndDetection.detect_text_elements
