from enum import Enum
from typing import Optional, Tuple

from cairosvg import svg2png
from userpic.blocks import generate_data
from userpic.svg import make_svg_data
from userpic.tools import random_bool

WHITE_COLOR = "#fff"


class AllowedFormats(str, Enum):
    PNG = "png"
    SVG = "svg"


class Userpic:
    def __init__(
        self,
        cells_count: int = 5,
        cell_size: int = 8,
        offset: int = 4,
    ):
        self.cells_count = cells_count
        self.cell_size = cell_size
        self.offset = offset

    @staticmethod
    def _random_color() -> str:
        return "f" if random_bool() else "6"

    @classmethod
    def _generate_random_color(cls) -> str:
        color = f"#{cls._random_color()}{cls._random_color()}{cls._random_color()}"
        if color == WHITE_COLOR:
            color = cls._generate_random_color()
        return color

    @property
    def preferred_colors(self) -> Tuple[str, str]:
        return WHITE_COLOR, self._generate_random_color()

    def make(
        self,
        first_color: Optional[str] = None,
        second_color: Optional[str] = None,
        data_format: AllowedFormats = AllowedFormats.PNG,
    ) -> bytes:
        raw = generate_data(
            cells_count=self.cells_count,
        )
        if (first_color or second_color) is None:
            first_color, second_color = self.preferred_colors
        data = make_svg_data(
            data=raw,
            cell_size=self.cell_size,
            offset=self.offset,
            first_color=first_color,
            second_color=second_color,
        )
        if data_format == data_format.PNG:
            return svg2png(data)  # type: ignore
        return data

    def save(
        self,
        filename: str,
        first_color: Optional[str] = None,
        second_color: Optional[str] = None,
        data_format: AllowedFormats = AllowedFormats.PNG,
    ) -> None:
        extension = f".{data_format.value.lower()}"
        if not filename.endswith(extension):
            filename += extension
        data = self.make(first_color, second_color, data_format)
        with open(filename, "wb") as file:
            file.write(data)
