# Userpic Generator

[![PyPI version](https://badge.fury.io/py/tiny-userpic.svg)](https://pypi.org/project/tiny-userpic/)

## Getting Started

## Installing

tiny-userpic can be installed using pip:

```bash
pip install tiny-userpic
```

## Usage

To test that installation was successful, try:

```bash
python -m userpic --output img.png
```

tiny-userpic can be used both from the command line and as a Python library.

```python
from userpic import make_userpic
data = make_userpic(
    cells_count=7,
    cell_size=32,
    offset=16,
    data_format="svg",
)
with open("output.svg", "wb") as file:
    file.write(data)
```
