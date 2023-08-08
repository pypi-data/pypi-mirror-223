# image2layout_computer_vision

An image processing module for some computer vision tasks (public module for image2layout)

Package Page: [pypi](https://pypi.org/project/image2layout-computer-vision/)

Features:

1. Text Detection and Recognition (OCR)
2. Color extraction (background and main foreground)

## Installations

### Install with `python`/`conda` [Linux]

1. (Optional) Conda

```bash
curl https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh -o ~/conda.sh
bash ~/conda.sh -b -f -p /opt/conda
rm ~/conda.sh
conda init --all --dry-run --verbose

conda create -n cv python=3.10 -y
conda activate cv
```

3. Python libraries (python>=3.8)

```bash
# python -m pip install 'torch>=2.0' torchvision torchaudio
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

python -m pip install datasets transformers scikit-learn
python -m pip install --upgrade datasets transformers scikit-learn Pillow numpy pandas
python -m pip install paddleocr paddlepaddle

python -m pip install --upgrade image2layout-computer-vision
```

### Install with `docker`
For running with CPU on Ubuntu
```bash
sudo docker build --tag cv -f Dockerfile_cpu .

sudo docker run -it -p 0.0.0.0:8000:8000 -p 0.0.0.0:8001:8001 -v $(pwd):/app cv bash

```

From inside container
```bash
cd deployment
conda activate cv
python api_serve.py -n CV -p 8000
```

## Usage

1. Run this python code to pre-download model weights

```python
from image2layout_computer_vision import model_dispatch
model_dispatch._load()
```

2. Recognize texts

```python
import image2layout_computer_vision as icv

# [A] text + box, 2 lists of dicts with keys [text, box, score]
data_merged, data_raw = icv.detect_text_full('path/to/image.png')

# [B] no text, only box -> 2 lists of dicts with keys [text, box, score]
data_merged, data_raw = icv.detect_text_boxes('path/to/image.png')

# [C] text + box -> list of dicts with keys [text, box, score]
data_raw = icv.detect_text_element('path/to/image.png')

# [D] text + box (multiple images) -> list of list of dicts with keys [text, box, score]
data_raw_multi = icv.detect_text_elements(['path/to/image.png', 'path/to/image2.png'])

```

3. Extract colors
```python
import image2layout_computer_vision as icv

# 2 rgb-color tuples for background and foreground
color_bg, color_fg = icv.extract_colors('path/to/image.png')
```



## Build
(for building and uploading this package)
```bash
python -m pip install --upgrade pip
python -m pip install --upgrade build twine "keyring<19.0"

rm -rf dist
python -m build
python -m twine upload dist/* --verbose
```
