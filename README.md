# 🖼️ Github-like userpics generator

Oversimplified Github-like userpics generation python library

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)
[![PyPI](https://img.shields.io/pypi/dm/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)

## Getting Started

## Installing

Library can be installed using pip:

```bash
pip install tiny-userpic
```

## Usage

```python
from userpic import make_userpic_image, make_userpic_svg

# make PIL Image object
image = make_userpic_image(
    size=(7, 5),
    padding=(20, 10),
    mode="RGBA",
    image_size=(300, 600),
)
# save as JPEG file
with open("output.jpeg", "wb") as fp:
    image.save(fp)
```

### Results:

![alt text](example.png)
