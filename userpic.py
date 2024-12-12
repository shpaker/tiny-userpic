from collections.abc import Generator
from random import getrandbits
from typing import Union

from PIL import ImageDraw
from PIL.Image import Image, _check_size
from PIL.Image import new as make_image

__all__ = ['__version__', 'make_userpic_image', 'make_userpic_svg']
__title__ = 'tiny-userpic'
__version__ = '0.0.0'
__url__ = 'https://github.com/shpaker/tiny-userpic'
__author__ = 'Aleksandr Shpak'
__author_email__ = 'shpaker@gmail.com'
__license__ = 'MIT'


def _iter_bits(n: int) -> Generator[int, None, None]:
    while n != 0:
        yield n & 1
        n = n >> 1


def _invert_bits(n: int, bits_num: int) -> int:
    result = 0
    shift = bits_num
    for i in _iter_bits(n):
        result = result << 1 | i
        shift -= 1
    return result << shift


def _iter_bit_lines(size: tuple[int, int] | list[int]) -> Generator[int, None, None]:
    bits_count = size[0] // 2
    with_spacer = size[0] % 2 == 1
    spacer = 0
    while not spacer:
        spacer = getrandbits(size[1])
    for i in range(size[1]):
        data = 0
        while not data:
            data = getrandbits(bits_count)
        inverted = _invert_bits(data, bits_count)
        if with_spacer:
            data = data << 1 | (spacer >> i & 1)
        yield data << bits_count | inverted


def _make_rectangles_xy(
    size: tuple[int, int] | list[int],
    image_size: tuple[int, int] | list[int],
    padding: tuple[int, int] | list[int],
) -> Generator[tuple[float, float, float, float], None, None]:
    _check_size(size)
    _check_size(padding)
    _check_size(image_size)
    rect_size = ((image_size[0] - 2 * padding[0]) / size[0], (image_size[1] - 2 * padding[1]) / size[1])
    for n, line in enumerate(_iter_bit_lines(size)):
        pos = size[0]
        for bit in _iter_bits(line):
            pos -= 1
            if not bit:
                continue
            x = padding[0] + pos * rect_size[0]
            y = padding[1] + n * rect_size[1]
            yield x, y, rect_size[0], rect_size[1]


def make_userpic_image(
    size: tuple[int, int] | list[int],
    mode: str,
    image_size: tuple[int, int] | list[int],
    padding: tuple[int, int] | list[int] = (0, 0),
    background: Union[float, tuple[int, ...], str] = 'white',
    foreground: Union[float, tuple[int, ...], str] = 'black',
) -> Image:
    image = make_image(mode=mode, size=image_size, color=background)
    draw = ImageDraw.Draw(image)
    for xy in _make_rectangles_xy(size=size, image_size=image_size, padding=padding):
        draw.rectangle((xy[0], xy[1], xy[0] + xy[2], xy[1] + xy[3]), width=0, fill=foreground)
    return image


def _make_svg_rectangle(xy: tuple[float, float, float, float], fill: float | tuple[float, ...] | str | None) -> str:
    return f'<rect x="{xy[0]}" y="{xy[1]}" width="{xy[2]}" height="{xy[3]}" style="fill:{fill}"/>'


def make_userpic_svg(
    size: tuple[int, int] | list[int],
    image_size: tuple[int, int] | list[int],
    padding: tuple[int, int] | list[int] = (0, 0),
    background: float | tuple[float, ...] | str | None = 'white',
    foreground: float | tuple[float, ...] | str | None = 'black',
) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        f'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
        f'<svg  version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0, 0, {image_size[0]}, {image_size[1]}">'
        f'{_make_svg_rectangle((0, 0, image_size[0], image_size[1]), fill=background) if background else ""}'
        f'{"".join([_make_svg_rectangle(xy, fill=foreground) for xy in _make_rectangles_xy(size=size, image_size=image_size, padding=padding)])}'
        f'</svg>'
    )
