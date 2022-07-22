from enum import Enum
from typing import Optional, Union

from userpic.blocks import generate_data
from userpic.svg import make_svg_data
from userpic.utils import preferred_colors

try:
    from cairosvg import svg2png
except ImportError:
    pass


class DataFormats(str, Enum):
    PNG = "png"
    SVG = "svg"


def make_userpic(
    cells_count: int = 5,
    cell_size: int = 16,
    offset: int = 8,
    data_format: Union[DataFormats, str] = DataFormats.PNG,
    first_color: Optional[str] = None,
    second_color: Optional[str] = None,
) -> bytes:
    if isinstance(data_format, str):
        data_format = DataFormats(data_format.lower())
    raw = generate_data(
        cells_count=cells_count,
    )
    if first_color is None or second_color is None:
        first_color, second_color = preferred_colors()
    data = make_svg_data(
        data=raw,
        cell_size=cell_size,
        offset=offset,
        first_color=first_color,
        second_color=second_color,
    )
    if data_format == DataFormats.PNG:
        return svg2png(data)  # type: ignore
    return data
