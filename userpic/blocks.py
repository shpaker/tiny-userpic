from typing import List

from userpic.tools import random_bool


def generate_row(
    cells_count: int,
) -> List[bool]:
    row = [random_bool() for _ in range(cells_count)]
    return row


def generate_block(
    width: int,
    height: int,
) -> List[List[bool]]:
    return [generate_row(width) for _ in range(height)]


def reverse_block(
    block: List[List[bool]],
) -> List[List[bool]]:
    return [list(reversed(i)) for i in block]


def concatenate_blocks(
    *blocks: List[List[bool]],
) -> List[List[bool]]:
    result: List[List[bool]] = list()
    for block in blocks:
        for i, row in enumerate(block):
            if len(result) - 1 < i:
                result.append(list())
            result[i] += row
    return result


def generate_data(
    cells_count: int = 5,
) -> List[List[bool]]:
    left = generate_block(width=cells_count // 2, height=cells_count)
    spacer = generate_block(width=cells_count % 2, height=cells_count)
    right = reverse_block(left)
    return concatenate_blocks(left, spacer, right)
