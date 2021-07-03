from typing import List, Optional

SVG_WRAPPER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="<http://www.w3.org/2000/svg>" viewBox="0, 0, {width}, {height}">
{rects}
</svg>
"""
SVG_RECT_TAG = (
    '<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:{color}" />'
)


def make_svg_cell(
    x: int,
    y: int,
    offset: int,
    size: int,
    color: Optional[str],
) -> str:
    return SVG_RECT_TAG.format(
        x=x * size + offset,
        y=y * size + offset,
        size=size,
        color=color,
    )


def make_svg_data(
    data: List[List[bool]],
    cell_size: int,
    offset: int,
    first_color: Optional[str],
    second_color: Optional[str],
) -> bytes:
    box_size = len(data) * cell_size + 2 * offset
    box = make_svg_cell(
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
            rect = make_svg_cell(
                x=x,
                y=y,
                offset=offset,
                size=cell_size,
                color=second_color,
            )
            rects.append(rect)
    svg_xml = SVG_WRAPPER.format(
        rects="\\n".join(rects),
        size=box_size,
        color=first_color,
    )
    return svg_xml.encode()
