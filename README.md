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

Requires Python 3.10 or newer.

```bash
pip install tiny-userpic
```

The package installs a single top-level module named `userpic`.

## Usage

The library provides several ways to generate avatars:

### 1. Random Generation (Non-deterministic)
Generate a unique random avatar each time.

```python
from userpic import make_userpic_image

# Generate random avatar
random_image = make_userpic_image(
    size=(7, 5),
    image_size=(300, 300),
    background="white",
    foreground="black"
)
random_image.save("random_avatar.png")
```

### 2. With Custom Seed (Deterministic)
Generate an avatar with a specific seed for reproducible results.

```python
from userpic import make_userpic_image, make_userpic_svg

# Generate avatar with specific seed
seeded_image = make_userpic_image(
    size=(7, 5),
    image_size=(300, 300),
    background="white",
    foreground="black",
    seed=42  # Any integer value will work as seed
)
seeded_image.save("seeded_avatar.png")

# The same seed produces the same pattern in SVG
seeded_svg = make_userpic_svg(size=(7, 5), image_size=(300, 300), seed=42)
```

### 3. From Text Input (Deterministic)
Generate an avatar from any text input (email, username, etc.). The same input will always produce the same avatar.

```python
from userpic import make_userpic_image_from_string, make_userpic_svg_from_string

# Generate avatar from email
email = "user@example.com"

# As PNG image
image = make_userpic_image_from_string(
    text=email,           # Input text to generate avatar from
    size=(7, 5),          # Pattern size (width, height)
    image_size=(300, 300),  # Output image size in pixels
    background="white",   # Background color (can be color name, hex or RGB tuple)
    foreground="black"    # Foreground color (can be color name, hex or RGB tuple)
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

### Common Parameters
All generation methods share these parameters:
- `size`: Tuple of (width, height) for the pattern size in cells (default: `(5, 5)`, width must be at least 2)
- `image_size`: Tuple of (width, height) for the output image size in pixels (default: `(300, 300)`)
- `background`: Background color (color name, hex string, RGB or RGBA tuple; `None` for no background in SVG)
- `foreground`: Foreground color (color name, hex string, RGB or RGBA tuple)
- `padding`: Padding around the pattern in pixels (default: `(20, 20)`)
- `mode`: Image mode for PNG output (default: `'RGB'`, can be `'RGBA'` for transparency)

The pattern must fit into the image: `image_size` minus twice the `padding` has to leave at least one pixel per
cell, otherwise a `ValueError` is raised.

## Examples

### Basic (from string)
![Basic example](examples/basic.png)

### Colored
![Colored example](examples/colored.png)

### Transparent
![Transparent example](examples/transparent.png)

### Small
![Small example](examples/small.png)

### Large
![Large example](examples/large.png)

### Seeded (deterministic)
![Seeded example](examples/seeded.png)
