# Github-like Userpic (Avatar) Generator

Oversimplified Github-like userpic (avatar) generator.

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)
[![PyPI](https://img.shields.io/pypi/dm/tiny-userpic.svg)](https://pypi.python.org/pypi/tiny-userpic)

## Features

- Generate unique avatars from text input (email, username, etc.)
- Create both PIL Image and SVG outputs
- Customizable size, colors, and padding
- Deterministic output (same input always produces the same avatar)

## Installation

```bash
pip install tiny-userpic
```

## Usage

```python
from tiny_userpic import make_userpic_image_from_string, make_userpic_svg_from_string

# Generate avatar from email
email = "user@example.com"

# As PNG image
image = make_userpic_image_from_string(
    text=email,
    size=(7, 5),          # Pattern size (width, height)
    image_size=(300, 300), # Output image size
    background="white",    # Background color
    foreground="black"     # Foreground color
)
image.save("avatar.png")

# As SVG
svg = make_userpic_svg_from_string(
    text=email,
    size=(7, 5),
    image_size=(300, 300),
    background="white",
    foreground="black"
)
with open("avatar.svg", "w") as f:
    f.write(svg)
```

## Examples

### Basic
![Basic example](examples/basic.png)

### Colored
![Colored example](examples/colored.png)

### Transparent
![Transparent example](examples/transparent.png)

### Small
![Small example](examples/small.png)

### Large
![Large example](examples/large.png)
