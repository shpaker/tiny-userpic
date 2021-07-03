from userpic.blocks import (
    generate_block,
    generate_row,
    reverse_block,
    concatenate_blocks,
    generate_data,
)


def test_generate_row() -> None:
    row = generate_row(cells_count=6)
    all_are_bool = all(isinstance(x, bool) for x in row)
    assert len(row) == 6, row
    assert all_are_bool is True, row


def test_generate_block() -> None:
    block = generate_block(4, 3)
    assert len(block) == 3, block
    equal_lengths = all(len(r) == 4 for r in block)
    assert equal_lengths is True, block


def test_reverse_block() -> None:
    block = generate_block(7, 8)
    reversed_block = [list(reversed(i)) for i in block]
    tested_block = reverse_block(block)
    assert tested_block == reversed_block, tested_block


def test_concatenate_blocks() -> None:
    rows_count = 3
    left_block = generate_block(7, rows_count)
    spacer = generate_block(1, rows_count)
    right_block = reverse_block(left_block)
    tested_block = concatenate_blocks(left_block, spacer, right_block)
    assert len(tested_block) == rows_count, tested_block
    for i in range(rows_count):
        expected_row = [
            *left_block[i],
            *spacer[i],
            *right_block[i],
        ]
        assert tested_block[i] == expected_row, expected_row


def test_generate_data() -> None:
    data = generate_data(3)
    assert len(data) == 3, data
    assert all(len(d)== 3 for d in data), data
