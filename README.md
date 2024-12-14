# Github-like userpic (avatar) generator

Oversimplified Github-like userpic (avatar) generator

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)
[![PyPI](https://img.shields.io/pypi/dm/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)

## Install from PyPI

Library can be installed using pip:

```bash
pip install tiny-userpic
```

## Generate PIL image

```python
from PIL.Image import Image

from userpic import make_userpic_image

# make PIL Image object
image: Image = make_userpic_image(
    size=(7, 5),
    padding=(20, 10),
    mode='RGB',
    image_size=(300, 300),
    background='white',
    foreground='black',
)

# save as JPEG file
with open('output.jpeg', 'wb') as fp:
    image.save(fp)
```

## Generate SVG data

```python

from userpic import make_userpic_svg

# make string data
image: str = make_userpic_svg(
  size=(7, 5),
  padding=(20, 10),
  image_size=(300, 300),
  background='white',
  foreground='black',
)

# save as SVG file
with open('output.svg', 'w') as fp:
  fp.write(image)
```

## The result should look something like this

![Awesome genearted userpic!](example.png)
