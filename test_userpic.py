from typing import Any

import pytest
from PIL.Image import Image

from userpic import (
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
