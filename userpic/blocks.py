from typing import List

from userpic.utils import random_bool


def _generate_row(
    cells_count: int,
) -> List[bool]:
    row = [random_bool() for _ in range(cells_count)]
    return row


def _generate_block(
    width: int,
    height: int,
) -> List[List[bool]]:
    return [_generate_row(width) for _ in range(height)]


def _reverse_block(
    block: List[List[bool]],
) -> List[List[bool]]:
    return [list(reversed(i)) for i in block]


def _concatenate_blocks(
    *blocks: List[List[bool]],
) -> List[List[bool]]:
    result: List[List[bool]] = []
    for block in blocks:
        for i, row in enumerate(block):
            if len(result) - 1 < i:
                result.append([])
            result[i] += row
    return result


def generate_data(
    cells_count: int = 5,
) -> List[List[bool]]:
    left = _generate_block(width=cells_count // 2, height=cells_count)
    spacer = _generate_block(width=cells_count % 2, height=cells_count)
    right = _reverse_block(left)
    return _concatenate_blocks(left, spacer, right)
