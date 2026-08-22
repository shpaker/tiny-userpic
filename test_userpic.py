import hashlib
import re
from collections.abc import Callable
from typing import Any
from xml.dom.minidom import parseString

import pytest
from PIL import ImageOps
from PIL.Image import Image

from userpic import (
    _cell_edges,
    _iter_bit_lines,
    make_userpic_image,
    make_userpic_image_from_string,
    make_userpic_svg,
    make_userpic_svg_from_string,
)


@pytest.fixture
def default_params() -> dict[str, Any]:
    return {
        'size': (7, 5),
        'image_size': (300, 300),
        'padding': (20, 20),
        'mode': 'RGB',
        'background': 'white',
        'foreground': 'black',
    }


def _svg_cells(svg: str) -> set[tuple[int, int]]:
    body = svg.split('<g ', 1)[1]
    cells: set[tuple[int, int]] = set()
    for x, y, span in re.findall(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="1"/>', body):
        cells.update((int(x) + offset, int(y)) for offset in range(int(span)))
    return cells


def _image_cells(
    image: Image,
    size: tuple[int, int],
    image_size: tuple[int, int],
    padding: tuple[int, int],
) -> set[tuple[int, int]]:
    cell_width = (image_size[0] - 2 * padding[0]) / size[0]
    cell_height = (image_size[1] - 2 * padding[1]) / size[1]
    return {
        (x, y)
        for y in range(size[1])
        for x in range(size[0])
        if image.getpixel(
            (int(padding[0] + (x + 0.5) * cell_width), int(padding[1] + (y + 0.5) * cell_height)),
        )
        == (0, 0, 0)
    }


def test_make_userpic_image(default_params: dict[str, Any]) -> None:
    image = make_userpic_image(**default_params)
    assert isinstance(image, Image)
    assert image.size == default_params['image_size']
    assert image.mode == default_params['mode']


def test_make_userpic_svg(default_params: dict[str, Any]) -> None:
    params = {k: v for k, v in default_params.items() if k != 'mode'}
    svg = make_userpic_svg(**params)
    assert isinstance(svg, str)
    assert '<svg' in svg
    assert 'rect' in svg


def test_seed_reproducibility(default_params: dict[str, Any]) -> None:
    seed = 42
    image1 = make_userpic_image(**default_params, seed=seed)
    image2 = make_userpic_image(**default_params, seed=seed)
    assert image1.tobytes() == image2.tobytes()


def test_different_seeds(default_params: dict[str, Any]) -> None:
    image1 = make_userpic_image(**default_params, seed=1)
    image2 = make_userpic_image(**default_params, seed=2)
    assert image1.tobytes() != image2.tobytes()


def test_string_based_image_consistency(default_params: dict[str, Any]) -> None:
    text = 'test@example.com'
    params = {k: v for k, v in default_params.items() if k not in ['seed']}
    image1 = make_userpic_image_from_string(text=text, **params)
    image2 = make_userpic_image_from_string(text=text, **params)
    assert image1.tobytes() == image2.tobytes()


def test_string_based_svg_consistency(default_params: dict[str, Any]) -> None:
    text = 'test@example.com'
    params = {k: v for k, v in default_params.items() if k not in ['seed', 'mode']}
    svg1 = make_userpic_svg_from_string(text=text, **params)
    svg2 = make_userpic_svg_from_string(text=text, **params)
    assert svg1 == svg2


def test_different_strings_different_results(default_params: dict[str, Any]) -> None:
    params = {k: v for k, v in default_params.items() if k not in ['seed']}
    image1 = make_userpic_image_from_string(text='user1@example.com', **params)
    image2 = make_userpic_image_from_string(text='user2@example.com', **params)
    assert image1.tobytes() != image2.tobytes()


@pytest.mark.parametrize(
    'size',
    [
        (5, 5),
        (7, 7),
        (9, 9),
    ],
)
def test_different_sizes(default_params: dict[str, Any], size: tuple[int, int]) -> None:
    params = default_params.copy()
    params['size'] = size
    image = make_userpic_image(**params)
    assert isinstance(image, Image)


@pytest.mark.parametrize('mode', ['RGB', 'RGBA', 'L'])
def test_different_modes(default_params: dict[str, Any], mode: str) -> None:
    params = default_params.copy()
    params['mode'] = mode
    image = make_userpic_image(**params)
    assert image.mode == mode


def test_svg_structure(default_params: dict[str, Any]) -> None:
    params = {k: v for k, v in default_params.items() if k != 'mode'}
    svg = make_userpic_svg(**params)
    assert '<svg' in svg
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg
    assert '</svg>' in svg
    assert 'rect' in svg


def test_empty_string() -> None:
    image = make_userpic_image_from_string(text='', size=(7, 5), mode='RGB', image_size=(300, 300))
    assert isinstance(image, Image)


@pytest.mark.parametrize(
    'size',
    [
        (7, 5),
        (8, 6),
        (5, 5),
        (2, 1),
    ],
)
@pytest.mark.parametrize('image_size', [(300, 300), (280, 300), (301, 299), (256, 256)])
def test_image_is_mirror_symmetric(size: tuple[int, int], image_size: tuple[int, int]) -> None:
    for seed in range(10):
        image = make_userpic_image(size=size, image_size=image_size, padding=(0, 0), seed=seed)
        assert image.tobytes() == ImageOps.mirror(image).tobytes()


@pytest.mark.parametrize('size', [(7, 5), (8, 6), (12, 12)])
def test_svg_matches_image(size: tuple[int, int]) -> None:
    image_size, padding = (300, 300), (20, 20)
    for seed in range(10):
        svg = make_userpic_svg(size=size, image_size=image_size, padding=padding, seed=seed)
        image = make_userpic_image(size=size, image_size=image_size, padding=padding, seed=seed)
        assert _svg_cells(svg) == _image_cells(image, size, image_size, padding)


@pytest.mark.parametrize(
    'color',
    [
        'red"/><script>alert(1)</script><rect fill="blue',
        "red'/><script/>",
        'red&<>',
    ],
)
def test_svg_escapes_colors(color: str) -> None:
    svg = make_userpic_svg(size=(5, 5), background=color, foreground=color, seed=1)
    assert '<script' not in svg
    parseString(svg)


@pytest.mark.parametrize(
    ('color', 'expected'),
    [
        ((12, 34, 56), 'rgb(12,34,56)'),
        ((0, 0, 128, 255), 'rgba(0,0,128,1)'),
        ((255, 255, 255, 0), 'rgba(255,255,255,0)'),
        ((128,), 'rgb(128,128,128)'),
    ],
)
def test_svg_renders_color_tuples(color: tuple[int, ...], expected: str) -> None:
    svg = make_userpic_svg(size=(5, 5), foreground=color, seed=1)
    assert f'fill="{expected}"' in svg


def test_svg_without_background() -> None:
    svg = make_userpic_svg(size=(5, 5), background=None, seed=1)
    assert 'width="100%"' not in svg
    parseString(svg)


def test_svg_is_well_formed(default_params: dict[str, Any]) -> None:
    params = {k: v for k, v in default_params.items() if k != 'mode'}
    parseString(make_userpic_svg(**params))


@pytest.mark.parametrize('maker', [make_userpic_image, make_userpic_svg])
@pytest.mark.parametrize(
    'params',
    [
        {'size': (1, 5)},
        {'size': (0, 5)},
        {'size': (5, 0)},
        {'size': (-5, 5)},
        {'size': (7.5, 5)},
        {'size': 'xx'},
        {'size': (7, 5, 3)},
        {'image_size': (0, 0)},
        {'image_size': (-10, -10)},
        {'padding': (-1, 0)},
        {'padding': (200, 200)},
        {'size': (1001, 1001)},
    ],
)
def test_invalid_geometry_is_rejected(maker: Callable[..., object], params: dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        maker(**params)


def test_string_based_svg_matches_seeded_svg() -> None:
    text = 'user@example.com'
    from_string = make_userpic_svg_from_string(text=text)
    seed = int.from_bytes(hashlib.sha256(text.encode('utf-8')).digest()[:8], byteorder='big')
    from_seed = make_userpic_svg(seed=seed)
    assert from_string == from_seed


def test_accepts_lists_as_sizes() -> None:
    assert isinstance(make_userpic_image(size=[7, 5], image_size=[300, 300], padding=[20, 20]), Image)
    assert make_userpic_svg(size=[7, 5], image_size=[300, 300], padding=[20, 20], seed=1).startswith('<svg')


@pytest.mark.parametrize('count', [2, 3, 5, 7, 8, 12, 16])
@pytest.mark.parametrize('extent', [16, 100, 250, 255, 256, 301])
def test_cell_edges_tile_the_axis(count: int, extent: int) -> None:
    offset = 7
    edges = _cell_edges(offset, extent, count)
    widths = [edges[index + 1] - edges[index] for index in range(count)]
    assert edges[0] == offset
    assert edges[-1] == offset + extent
    assert min(widths) >= 1
    if not (count % 2 == 0 and extent % 2 == 1):
        assert widths == widths[::-1]


@pytest.mark.parametrize(
    ('size', 'image_size', 'padding'),
    [
        ((12, 12), (300, 300), (25, 25)),
        ((12, 12), (420, 420), (25, 25)),
        ((7, 5), (300, 300), (20, 20)),
        ((5, 5), (64, 64), (0, 0)),
        ((16, 3), (301, 301), (1, 1)),
        ((10, 10), (255, 255), (0, 0)),
    ],
)
def test_adjacent_cells_are_not_separated_by_a_seam(
    size: tuple[int, int],
    image_size: tuple[int, int],
    padding: tuple[int, int],
) -> None:
    """Two neighbouring filled cells must be painted as one solid block.

    The cell centres are derived from the plain geometry rather than from the module internals, so
    the test stays independent of how the cell boundaries are computed.
    """
    cell_width = (image_size[0] - 2 * padding[0]) / size[0]
    cell_height = (image_size[1] - 2 * padding[1]) / size[1]

    def centre(column: int, row: int) -> tuple[int, int]:
        return (
            int(padding[0] + (column + 0.5) * cell_width),
            int(padding[1] + (row + 0.5) * cell_height),
        )

    for seed in range(5):
        image = make_userpic_image(size=size, image_size=image_size, padding=padding, seed=seed)
        lines = list(_iter_bit_lines(size, seed=seed))
        filled = {
            (column, row)
            for row, line in enumerate(lines)
            for column in range(size[0])
            if line >> (size[0] - 1 - column) & 1
        }
        for column, row in filled:
            if (column + 1, row) in filled:
                x_from, y = centre(column, row)
                x_to, _ = centre(column + 1, row)
                painted = [image.getpixel((x, y)) for x in range(x_from, x_to + 1)]
                assert painted == [(0, 0, 0)] * len(painted)
            if (column, row + 1) in filled:
                x, y_from = centre(column, row)
                _, y_to = centre(column, row + 1)
                painted = [image.getpixel((x, y)) for y in range(y_from, y_to + 1)]
                assert painted == [(0, 0, 0)] * len(painted)


@pytest.mark.parametrize(
    ('size', 'image_size', 'padding'),
    [
        ((7, 5), (300, 300), (20, 20)),
        ((12, 12), (300, 300), (25, 25)),
        ((5, 5), (128, 128), (7, 7)),
    ],
)
def test_padding_is_never_painted_over(
    size: tuple[int, int],
    image_size: tuple[int, int],
    padding: tuple[int, int],
) -> None:
    for seed in range(5):
        image = make_userpic_image(size=size, image_size=image_size, padding=padding, seed=seed)
        border = (
            [(x, y) for y in range(padding[1]) for x in range(image_size[0])]
            + [(x, y) for y in range(image_size[1] - padding[1], image_size[1]) for x in range(image_size[0])]
            + [(x, y) for x in range(padding[0]) for y in range(image_size[1])]
            + [(x, y) for x in range(image_size[0] - padding[0], image_size[0]) for y in range(image_size[1])]
        )
        assert all(image.getpixel(point) == (255, 255, 255) for point in border)
