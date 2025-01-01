# Github-like Userpic (Avatar) Generator

Oversimplified Github-like userpic (avatar) generator.

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)
[![PyPI](https://img.shields.io/pypi/dm/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)

## Installation

Get started by installing the library via pip:

```bash
pip install tiny-userpic
```

## Create a PIL Image

```python
from PIL.Image import Image

from userpic import make_userpic_image

# Generate a PIL Image object
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

## Create SVG Data

```python

from userpic import make_userpic_svg

# Generate SVG string data
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

## Example Output

Check out the awesome userpic you can generate:

![Awesome generated userpic!](example.png)
