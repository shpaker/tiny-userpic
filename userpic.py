import hashlib
from collections.abc import Generator
from random import Random

from PIL import ImageDraw
from PIL.Image import Image as PILImage
from PIL.Image import _check_size
from PIL.Image import new as make_image

__all__ = [
    '__author__',
    '__author_email__',
    '__license__',
    '__title__',
    '__url__',
    '__version__',
    'make_userpic_image',
    'make_userpic_image_from_string',
    'make_userpic_svg',
    'make_userpic_svg_from_string',
]
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


def _iter_bit_lines(size: tuple[int, int] | list[int], seed: int | None = None) -> Generator[int, None, None]:
    """
    Generate lines of bits for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.
        seed (int | None, optional): Seed for random number generation. Defaults to None.

    Yields:
        int: The next line of bits.
    """
    rng = Random(seed) if seed is not None else Random()
    bits_count = size[0] // 2
    with_spacer = size[0] % 2 == 1
    spacer = 0
    while not spacer:
        spacer = rng.getrandbits(size[1])
    for i in range(size[1]):
        data = 0
        while not data:
            data = rng.getrandbits(bits_count)
        inverted = _invert_bits(data, bits_count)
        if with_spacer:
            data = data << 1 | (spacer >> i & 1)
        yield data << bits_count | inverted


def _make_rectangles_xy(
    size: tuple[int, int] | list[int],
    image_size: tuple[int, int] | list[int],
    padding: tuple[int, int] | list[int],
    seed: int | None = None,
) -> Generator[tuple[float, float, float, float], None, None]:
    """
    Generate the coordinates and sizes of rectangles for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.
        image_size (tuple[int, int] | list[int]): The size of the image.
        padding (tuple[int, int] | list[int]): The padding around the userpic.
        seed (int | None, optional): Seed for random number generation. Defaults to None.

    Yields:
        tuple[float, float, float, float]: The coordinates and size of the next rectangle.

    Raises:
        ValueError: If any of the size parameters are invalid.
    """
    _check_size(size)
    _check_size(padding)
    _check_size(image_size)

    rect_size = ((image_size[0] - 2 * padding[0]) / size[0], (image_size[1] - 2 * padding[1]) / size[1])
    for n, line in enumerate(_iter_bit_lines(size, seed=seed)):
        pos = size[0]
        for bit in _iter_bits(line):
            pos -= 1
            if not bit:
                continue
            x = padding[0] + pos * rect_size[0]
            y = padding[1] + n * rect_size[1]
            yield x, y, rect_size[0], rect_size[1]


def make_userpic_image(
    size: tuple[int, int],
    mode: str = 'RGB',
    image_size: tuple[int, int] = (300, 300),
    padding: tuple[int, int] = (20, 20),
    background: str | tuple[int, ...] = 'white',
    foreground: str | tuple[int, ...] = 'black',
    seed: int | None = None,
) -> PILImage:
    """
    Generate a PIL Image object for the userpic.

    Args:
        size (tuple[int, int]): The size of the userpic.
        mode (str): The mode of the image (e.g., 'RGB').
        image_size (tuple[int, int]): The size of the image.
        padding (tuple[int, int]): The padding around the userpic.
        background (str | tuple[int, ...]): The background color.
        foreground (str | tuple[int, ...]): The foreground color.
        seed (int | None, optional): Seed for random number generation. Defaults to None.

    Returns:
        Image: The generated PIL Image object.
    """
    image = make_image(mode=mode, size=image_size, color=background)
    draw = ImageDraw.Draw(image)
    for xy in _make_rectangles_xy(size=size, image_size=image_size, padding=padding, seed=seed):
        draw.rectangle((xy[0], xy[1], xy[0] + xy[2], xy[1] + xy[3]), width=0, fill=foreground)
    return image


def _make_svg_rectangle(xy: tuple[float, float, float, float], fill: float | tuple[float, ...] | str | None) -> str:
    """
    Generate an SVG rectangle element.

    Args:
        xy (Tuple[float, float, float, float]): The coordinates and size of the rectangle.
        fill (Union[float, Tuple[float, ...], str, None]): The fill color of the rectangle.

    Returns:
        str: The SVG rectangle element as a string.
    """
    return f'<rect x="{xy[0]}" y="{xy[1]}" width="{xy[2]}" height="{xy[3]}" style="fill:{fill}"/>'


def make_userpic_svg(
    size: tuple[int, int] | list[int] = (5, 5),
    image_size: tuple[int, int] | list[int] = (300, 300),
    padding: tuple[int, int] | list[int] = (0, 0),
    background: float | tuple[float, ...] | str | None = 'white',
    foreground: float | tuple[float, ...] | str | None = 'black',
    seed: int | None = None,
) -> str:
    """
    Generate an SVG string for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.
        image_size (tuple[int, int] | list[int]): The size of the image.
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (0, 0).
        background (float | tuple[float, ...] | str | None, optional): The background color. Defaults to 'white'.
        foreground (float | tuple[float, ...] | str | None, optional): The foreground color. Defaults to 'black'.
        seed (int | None, optional): Seed for random number generation. Defaults to None.

    Returns:
        str: The generated SVG string.
    """
    # Calculate pattern size and position
    pattern_width = image_size[0] - 2 * padding[0]
    pattern_height = image_size[1] - 2 * padding[1]
    cell_width = pattern_width / size[0]
    cell_height = pattern_height / size[1]

    # Generate SVG
    svg = f'<svg width="{image_size[0]}" height="{image_size[1]}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += f'<rect width="100%" height="100%" fill="{background}"/>\n'

    # Draw pattern
    for y, bits in enumerate(_iter_bit_lines(size, seed)):
        for x in range(size[0]):
            if bits & (1 << (size[0] - 1 - x)):
                svg += f'<rect x="{padding[0] + x * cell_width}" y="{padding[1] + y * cell_height}" width="{cell_width}" height="{cell_height}" fill="{foreground}"/>\n'

    svg += '</svg>'
    return svg


def _string_to_seed(text: str) -> int:
    """
    Convert a string to a stable seed value.

    Args:
        text (str): The input string (e.g., email or username).

    Returns:
        int: A stable seed value derived from the input string.
    """
    # Используем первые 8 байт SHA-256 хэша для получения 64-битного целого числа
    hash_bytes = hashlib.sha256(text.encode('utf-8')).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder='big')


def make_userpic_image_from_string(
    text: str,
    size: tuple[int, int] = (5, 5),
    mode: str = 'RGB',
    image_size: tuple[int, int] = (300, 300),
    padding: tuple[int, int] = (0, 0),
    background: str | tuple[int, ...] = 'white',
    foreground: str | tuple[int, ...] = 'black',
) -> PILImage:
    """
    Generate a PIL Image object for the userpic based on a string input.

    Args:
        text (str): The input string to generate the avatar from (e.g., email or username).
        size (tuple[int, int] | list[int]): The size of the userpic.
        mode (str): The mode of the image (e.g., 'RGB').
        image_size (tuple[int, int] | list[int], optional): The size of the image. Defaults to (300, 300).
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (0, 0).
        background (float | tuple[int, ...] | str, optional): The background color. Defaults to 'white'.
        foreground (float | tuple[int, ...] | str, optional): The foreground color. Defaults to 'black'.

    Returns:
        Image: The generated PIL Image object.
    """
    seed = _string_to_seed(text)
    return make_userpic_image(
        size=size,
        mode=mode,
        image_size=image_size,
        padding=padding,
        background=background,
        foreground=foreground,
        seed=seed,
    )


def make_userpic_svg_from_string(
    text: str,
    size: tuple[int, int] | list[int] = (5, 5),
    image_size: tuple[int, int] | list[int] = (300, 300),
    padding: tuple[int, int] | list[int] = (0, 0),
    background: float | tuple[float, ...] | str | None = 'white',
    foreground: float | tuple[float, ...] | str | None = 'black',
) -> str:
    """
    Generate an SVG string for the userpic based on a string input.

    Args:
        text (str): The input string to generate the avatar from (e.g., email or username).
        size (tuple[int, int] | list[int]): The size of the userpic.
        image_size (tuple[int, int] | list[int]): The size of the image.
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (0, 0).
        background (float | tuple[float, ...] | str | None, optional): The background color. Defaults to 'white'.
        foreground (float | tuple[float, ...] | str | None, optional): The foreground color. Defaults to 'black'.

    Returns:
        str: The generated SVG string.
    """
    seed = _string_to_seed(text)
    return make_userpic_svg(
        size=size,
        image_size=image_size,
        padding=padding,
        background=background,
        foreground=foreground,
        seed=seed,
    )


def make_userpic(
    size: tuple[int, int],
    mode: str = 'RGB',
    image_size: tuple[int, int] = (300, 300),
    padding: tuple[int, int] = (20, 20),
    background: str | tuple[int, ...] = 'white',
    foreground: str | tuple[int, ...] = 'black',
) -> PILImage:
    """
    Generate a PIL Image object for the userpic.

    Args:
        size (tuple[int, int]): The size of the userpic.
        mode (str): The mode of the image (e.g., 'RGB').
        image_size (tuple[int, int]): The size of the image.
        padding (tuple[int, int]): The padding around the userpic.
        background (str | tuple[int, ...]): The background color.
        foreground (str | tuple[int, ...]): The foreground color.

    Returns:
        Image: The generated PIL Image object.
    """
    return make_userpic_image(
        size=size,
        mode=mode,
        image_size=image_size,
        padding=padding,
        background=background,
        foreground=foreground,
    )
