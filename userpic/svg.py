from typing import List

_SVG_WRAPPER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg  version="1.1"
    xmlns="http://www.w3.org/2000/svg" viewBox="0, 0, {width}, {height}">
{rects}
</svg>
"""
_SVG_RECT_TAG = (
    '<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:{color}" />'
)


def _make_svg_cell(
    x: int,
    y: int,
    size: int,
    offset: int,
    color: str,
) -> str:
    return _SVG_RECT_TAG.format(
        x=x * size + offset,
        y=y * size + offset,
        width=size,
        height=size,
        color=color,
    )


def make_svg_data(
    data: List[List[bool]],
    cell_size: int,
    offset: int,
    first_color: str,
    second_color: str,
) -> bytes:
    box_size = len(data) * cell_size + 2 * offset
    box = _make_svg_cell(
        x=0,
        y=0,
        offset=0,
        size=box_size,
        color=first_color,
    )
    rects: List[str] = [box]
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if not cell:
                continue
            rect = _make_svg_cell(
                x=x,
                y=y,
                offset=offset,
                size=cell_size,
                color=second_color,
            )
            rects.append(rect)
    svg_xml = _SVG_WRAPPER.format(
        rects="\n".join(rects),
        width=box_size,
        height=box_size,
        color=first_color,
    )
    return svg_xml.encode()
