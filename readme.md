# Userpic Generator

## Installation

```bash
pip install tiny-userpic
```

## Usage

```bash
python -m userpic --output img.png
```

or

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
