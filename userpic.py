from collections.abc import Generator
from random import getrandbits

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
    """
    Iterate over the bits of an integer.

    Args:
        n (int): The integer to iterate over.

    Yields:
        int: The next bit (0 or 1).
    """
    while n != 0:
        yield n & 1
        n = n >> 1


def _invert_bits(n: int, bits_num: int) -> int:
    """
    Invert the bits of an integer.

    Args:
        n (int): The integer to invert.
        bits_num (int): The number of bits to consider.

    Returns:
        int: The inverted integer.
    """
    result = 0
    shift = bits_num
    for i in _iter_bits(n):
        result = result << 1 | i
        shift -= 1
    return result << shift


def _iter_bit_lines(size: tuple[int, int] | list[int]) -> Generator[int, None, None]:
    """
    Generate lines of bits for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.

    Yields:
        int: The next line of bits.
    """
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
    """
    Generate the coordinates and sizes of rectangles for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.
        image_size (tuple[int, int] | list[int]): The size of the image.
        padding (tuple[int, int] | list[int]): The padding around the userpic.

    Yields:
        tuple[float, float, float, float]: The coordinates and size of the next rectangle.
    """
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
    background: float | tuple[int, ...] | str = 'white',
    foreground: float | tuple[int, ...] | str = 'black',
) -> Image:
    """
    Generate a PIL Image object for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.
        mode (str): The mode of the image (e.g., 'RGB').
        image_size (tuple[int, int] | list[int]): The size of the image.
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (0, 0).
        background (float | tuple[int, ...] | str, optional): The background color. Defaults to 'white'.
        foreground (float | tuple[int, ...] | str, optional): The foreground color. Defaults to 'black'.

    Returns:
        Image: The generated PIL Image object.
    """
    image = make_image(mode=mode, size=image_size, color=background)
    draw = ImageDraw.Draw(image)
    for xy in _make_rectangles_xy(size=size, image_size=image_size, padding=padding):
        draw.rectangle((xy[0], xy[1], xy[0] + xy[2], xy[1] + xy[3]), width=0, fill=foreground)
    return image


def _make_svg_rectangle(xy: tuple[float, float, float, float], fill: float | tuple[float, ...] | str | None) -> str:
    """
    Generate an SVG rectangle element.

    Args:
        xy (tuple[float, float, float, float]): The coordinates and size of the rectangle.
        fill (float | tuple[float, ...] | str | None): The fill color of the rectangle.

    Returns:
        str: The SVG rectangle element as a string.
    """
    return f'<rect x="{xy[0]}" y="{xy[1]}" width="{xy[2]}" height="{xy[3]}" style="fill:{fill}"/>'


def make_userpic_svg(
    size: tuple[int, int] | list[int],
    image_size: tuple[int, int] | list[int],
    padding: tuple[int, int] | list[int] = (0, 0),
    background: float | tuple[float, ...] | str | None = 'white',
    foreground: float | tuple[float, ...] | str | None = 'black',
) -> str:
    """
    Generate an SVG string for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.
        image_size (tuple[int, int] | list[int]): The size of the image.
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (0, 0).
        background (float | tuple[float, ...] | str | None, optional): The background color. Defaults to 'white'.
        foreground (float | tuple[float, ...] | str | None, optional): The foreground color. Defaults to 'black'.

    Returns:
        str: The generated SVG string.
    """
    return (
        f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        f'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
        f'<svg  version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0, 0, {image_size[0]}, {image_size[1]}">'
        f'{_make_svg_rectangle((0, 0, image_size[0], image_size[1]), fill=background) if background else ""}'
        f'{"".join([_make_svg_rectangle(xy, fill=foreground) for xy in _make_rectangles_xy(size=size, image_size=image_size, padding=padding)])}'
        f'</svg>'
    )
