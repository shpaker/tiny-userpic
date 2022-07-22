from userpic.svg import _make_svg_cell, make_svg_data

_EXPECTED_SVG = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg  version="1.1"
    xmlns="http://www.w3.org/2000/svg" viewBox="0, 0, 8, 8">
<rect x="0" y="0" width="8" height="8" style="fill:red" />
<rect x="1" y="1" width="2" height="2" style="fill:blue" />
<rect x="5" y="1" width="2" height="2" style="fill:blue" />
<rect x="3" y="3" width="2" height="2" style="fill:blue" />
<rect x="1" y="5" width="2" height="2" style="fill:blue" />
<rect x="5" y="5" width="2" height="2" style="fill:blue" />
</svg>
"""


def test_make_svg_cell() -> None:
    cell = _make_svg_cell(1, 2, 5, 4, "red")
    assert cell == '<rect x="9" y="14" width="5" height="5" style="fill:red" />'


def test_make_svg_data() -> None:
    data = [
        [True, False, True],
        [False, True, False],
        [True, False, True],
    ]
    svg = make_svg_data(data, 2, 1, "red", "blue")

    assert svg.decode().strip() == _EXPECTED_SVG.strip()
