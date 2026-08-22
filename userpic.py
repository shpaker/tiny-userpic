import hashlib
from collections.abc import Generator, Sequence
from random import Random
from xml.sax.saxutils import escape

from PIL import ImageDraw
from PIL.Image import Image as PILImage
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

_PAIR_LENGTH = 2
_MIN_PATTERN_WIDTH = 2
_MIN_PATTERN_HEIGHT = 1
_GRAYSCALE_CHANNELS = 1
_RGB_CHANNELS = 3
_RGBA_CHANNELS = 4
_OPAQUE = 255
_SVG_ENTITIES = {'"': '&quot;', "'": '&apos;'}


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


def _iter_bit_runs(line: int, width: int) -> Generator[tuple[int, int], None, None]:
    """
    Iterate over runs of adjacent set bits in a line, left to right.

    Args:
        line (int): The line of bits.
        width (int): The number of bits in the line.

    Yields:
        tuple[int, int]: The offset and the length of the next run.
    """
    start = None
    for pos in range(width):
        if line >> (width - 1 - pos) & 1:
            if start is None:
                start = pos
            continue
        if start is not None:
            yield start, pos - start
            start = None
    if start is not None:
        yield start, width - start


def _check_pair(value: Sequence[int], name: str) -> None:
    """
    Check that a value is a pair of integers.

    Args:
        value (Sequence[int]): The value to check.
        name (str): The name of the parameter, used in the error message.

    Raises:
        ValueError: If the value is not a sequence of two integers.
    """
    if not isinstance(value, list | tuple) or len(value) != _PAIR_LENGTH:
        msg = f'{name} must be a sequence of two integers, got {value!r}'
        raise ValueError(msg)
    if not all(isinstance(item, int) for item in value):
        msg = f'{name} must contain integers only, got {value!r}'
        raise ValueError(msg)


def _check_geometry(
    size: tuple[int, int] | list[int],
    image_size: tuple[int, int] | list[int],
    padding: tuple[int, int] | list[int],
) -> tuple[int, int]:
    """
    Check that the requested pattern fits into the image and measure the pattern.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic pattern, in cells.
        image_size (tuple[int, int] | list[int]): The size of the image, in pixels.
        padding (tuple[int, int] | list[int]): The padding around the pattern, in pixels.

    Returns:
        tuple[int, int]: The width and the height of the pattern, in pixels.

    Raises:
        ValueError: If any of the size parameters are invalid or the pattern does not fit.
    """
    _check_pair(size, 'size')
    _check_pair(image_size, 'image_size')
    _check_pair(padding, 'padding')
    if size[0] < _MIN_PATTERN_WIDTH or size[1] < _MIN_PATTERN_HEIGHT:
        msg = f'size must be at least ({_MIN_PATTERN_WIDTH}, {_MIN_PATTERN_HEIGHT}), got {tuple(size)!r}'
        raise ValueError(msg)
    if image_size[0] < 1 or image_size[1] < 1:
        msg = f'image_size must be positive, got {tuple(image_size)!r}'
        raise ValueError(msg)
    if padding[0] < 0 or padding[1] < 0:
        msg = f'padding must be non-negative, got {tuple(padding)!r}'
        raise ValueError(msg)
    pattern_width = image_size[0] - 2 * padding[0]
    pattern_height = image_size[1] - 2 * padding[1]
    if pattern_width < size[0] or pattern_height < size[1]:
        msg = (
            f'image_size {tuple(image_size)!r} with padding {tuple(padding)!r} leaves '
            f'{pattern_width}x{pattern_height}px for a {size[0]}x{size[1]} pattern, '
            f'at least {size[0]}x{size[1]}px is required'
        )
        raise ValueError(msg)
    return pattern_width, pattern_height


def _cell_edges(offset: int, extent: int, count: int) -> list[int]:
    """
    Measure the pixel boundaries of the cells along one axis.

    Every boundary is derived from the same expression, so the right edge of a cell is always the
    left edge of the next one and the cells tile the pattern without gaps or overlaps.

    Args:
        offset (int): The position of the first boundary, in pixels.
        extent (int): The length of the pattern along the axis, in pixels.
        count (int): The number of cells along the axis.

    Returns:
        list[int]: The ``count + 1`` boundaries of the cells, in pixels.
    """
    return [offset + round(index * extent / count) for index in range(count + 1)]


def _iter_bit_lines(size: tuple[int, int] | list[int], seed: int | None = None) -> Generator[int, None, None]:
    """
    Generate lines of bits for the userpic.

    Args:
        size (tuple[int, int] | list[int]): The size of the userpic.
        seed (int | None, optional): Seed for random number generation. Defaults to None.

    Yields:
        int: The next line of bits.
    """
    rng = Random(seed)
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


def make_userpic_image(
    size: tuple[int, int] | list[int] = (5, 5),
    mode: str = 'RGB',
    image_size: tuple[int, int] | list[int] = (300, 300),
    padding: tuple[int, int] | list[int] = (20, 20),
    background: str | tuple[int, ...] = 'white',
    foreground: str | tuple[int, ...] = 'black',
    seed: int | None = None,
) -> PILImage:
    """
    Generate a PIL Image object for the userpic.

    Args:
        size (tuple[int, int] | list[int], optional): The size of the userpic. Defaults to (5, 5).
        mode (str, optional): The mode of the image (e.g., 'RGB'). Defaults to 'RGB'.
        image_size (tuple[int, int] | list[int], optional): The size of the image. Defaults to (300, 300).
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (20, 20).
        background (str | tuple[int, ...], optional): The background color. Defaults to 'white'.
        foreground (str | tuple[int, ...], optional): The foreground color. Defaults to 'black'.
        seed (int | None, optional): Seed for random number generation. Defaults to None.

    Returns:
        Image: The generated PIL Image object.

    Raises:
        ValueError: If any of the size parameters are invalid.
    """
    pattern_width, pattern_height = _check_geometry(size, image_size, padding)
    columns = _cell_edges(padding[0], pattern_width, size[0])
    rows = _cell_edges(padding[1], pattern_height, size[1])
    image = make_image(mode=mode, size=(image_size[0], image_size[1]), color=background)
    draw = ImageDraw.Draw(image)
    for row, line in enumerate(_iter_bit_lines(size, seed=seed)):
        for pos, span in _iter_bit_runs(line, size[0]):
            # the coordinates of ImageDraw.rectangle are inclusive on both ends
            draw.rectangle(
                (columns[pos], rows[row], columns[pos + span] - 1, rows[row + 1] - 1),
                width=0,
                fill=foreground,
            )
    return image


def _format_number(value: float) -> str:
    """
    Format a number for an SVG attribute, dropping insignificant digits.

    Args:
        value (float): The number to format.

    Returns:
        str: The formatted number.
    """
    return f'{value:.10g}'


def _format_svg_color(color: float | tuple[float, ...] | str | None) -> str:
    """
    Convert a color into an SVG paint value safe to embed into an attribute.

    Args:
        color (float | tuple[float, ...] | str | None): The color to convert.

    Returns:
        str: The SVG paint value.

    Raises:
        ValueError: If the color is a tuple of an unsupported length.
    """
    if color is None:
        return 'none'
    if isinstance(color, list | tuple):
        channels = tuple(color)
        if len(channels) == _GRAYSCALE_CHANNELS:
            channels = channels * _RGB_CHANNELS
        if len(channels) == _RGB_CHANNELS:
            red, green, blue = channels
            return f'rgb({int(red)},{int(green)},{int(blue)})'
        if len(channels) == _RGBA_CHANNELS:
            red, green, blue, alpha = channels
            return f'rgba({int(red)},{int(green)},{int(blue)},{alpha / _OPAQUE:.4g})'
        msg = f'color must have 1, 3 or 4 channels, got {color!r}'
        raise ValueError(msg)
    if isinstance(color, int | float):
        value = int(color)
        return f'rgb({value},{value},{value})'
    return escape(color, _SVG_ENTITIES)


def make_userpic_svg(
    size: tuple[int, int] | list[int] = (5, 5),
    image_size: tuple[int, int] | list[int] = (300, 300),
    padding: tuple[int, int] | list[int] = (20, 20),
    background: float | tuple[float, ...] | str | None = 'white',
    foreground: float | tuple[float, ...] | str | None = 'black',
    seed: int | None = None,
) -> str:
    """
    Generate an SVG string for the userpic.

    Args:
        size (tuple[int, int] | list[int], optional): The size of the userpic. Defaults to (5, 5).
        image_size (tuple[int, int] | list[int], optional): The size of the image. Defaults to (300, 300).
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (20, 20).
        background (float | tuple[float, ...] | str | None, optional): The background color. Defaults to 'white'.
        foreground (float | tuple[float, ...] | str | None, optional): The foreground color. Defaults to 'black'.
        seed (int | None, optional): Seed for random number generation. Defaults to None.

    Returns:
        str: The generated SVG string.

    Raises:
        ValueError: If any of the size parameters are invalid.
    """
    pattern_width, pattern_height = _check_geometry(size, image_size, padding)
    cell_width, cell_height = pattern_width / size[0], pattern_height / size[1]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{image_size[0]}" height="{image_size[1]}"'
        f' viewBox="0 0 {image_size[0]} {image_size[1]}" shape-rendering="crispEdges">'
    ]
    if background is not None:
        parts.append(f'<rect width="100%" height="100%" fill="{_format_svg_color(background)}"/>')
    # the pattern is drawn in cell units and scaled up, so the coordinates stay exact
    parts.append(
        f'<g fill="{_format_svg_color(foreground)}"'
        f' transform="translate({_format_number(padding[0])},{_format_number(padding[1])})'
        f' scale({_format_number(cell_width)},{_format_number(cell_height)})">'
    )
    for row, line in enumerate(_iter_bit_lines(size, seed=seed)):
        parts += [
            f'<rect x="{pos}" y="{row}" width="{span}" height="1"/>' for pos, span in _iter_bit_runs(line, size[0])
        ]
    parts.append('</g></svg>')
    return ''.join(parts)


def _string_to_seed(text: str) -> int:
    """
    Convert a string to a stable seed value.

    Args:
        text (str): The input string (e.g., email or username).

    Returns:
        int: A stable seed value derived from the input string.
    """
    # the first 8 bytes of the SHA-256 digest make up a 64-bit integer
    hash_bytes = hashlib.sha256(text.encode('utf-8')).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder='big')


def make_userpic_image_from_string(
    text: str,
    size: tuple[int, int] | list[int] = (5, 5),
    mode: str = 'RGB',
    image_size: tuple[int, int] | list[int] = (300, 300),
    padding: tuple[int, int] | list[int] = (20, 20),
    background: str | tuple[int, ...] = 'white',
    foreground: str | tuple[int, ...] = 'black',
) -> PILImage:
    """
    Generate a PIL Image object for the userpic based on a string input.

    Args:
        text (str): The input string to generate the avatar from (e.g., email or username).
        size (tuple[int, int] | list[int], optional): The size of the userpic. Defaults to (5, 5).
        mode (str, optional): The mode of the image (e.g., 'RGB'). Defaults to 'RGB'.
        image_size (tuple[int, int] | list[int], optional): The size of the image. Defaults to (300, 300).
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (20, 20).
        background (str | tuple[int, ...], optional): The background color. Defaults to 'white'.
        foreground (str | tuple[int, ...], optional): The foreground color. Defaults to 'black'.

    Returns:
        Image: The generated PIL Image object.

    Raises:
        ValueError: If any of the size parameters are invalid.
    """
    return make_userpic_image(
        size=size,
        mode=mode,
        image_size=image_size,
        padding=padding,
        background=background,
        foreground=foreground,
        seed=_string_to_seed(text),
    )


def make_userpic_svg_from_string(
    text: str,
    size: tuple[int, int] | list[int] = (5, 5),
    image_size: tuple[int, int] | list[int] = (300, 300),
    padding: tuple[int, int] | list[int] = (20, 20),
    background: float | tuple[float, ...] | str | None = 'white',
    foreground: float | tuple[float, ...] | str | None = 'black',
) -> str:
    """
    Generate an SVG string for the userpic based on a string input.

    Args:
        text (str): The input string to generate the avatar from (e.g., email or username).
        size (tuple[int, int] | list[int], optional): The size of the userpic. Defaults to (5, 5).
        image_size (tuple[int, int] | list[int], optional): The size of the image. Defaults to (300, 300).
        padding (tuple[int, int] | list[int], optional): The padding around the userpic. Defaults to (20, 20).
        background (float | tuple[float, ...] | str | None, optional): The background color. Defaults to 'white'.
        foreground (float | tuple[float, ...] | str | None, optional): The foreground color. Defaults to 'black'.

    Returns:
        str: The generated SVG string.

    Raises:
        ValueError: If any of the size parameters are invalid.
    """
    return make_userpic_svg(
        size=size,
        image_size=image_size,
        padding=padding,
        background=background,
        foreground=foreground,
        seed=_string_to_seed(text),
    )
