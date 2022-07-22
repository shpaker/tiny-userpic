from pathlib import Path
from typing import Tuple

from click import command, echo, option
from userpic import DataFormats, make_userpic

_DEFAULT_DATA_FORMAT = DataFormats.SVG
_DEFAULT_CELLS_COUNT = 5
_DEFAULT_CELL_SIZE = 32


def _check_filename(filename: str) -> Tuple[str, DataFormats]:
    parts = filename.split(".")
    if len(parts) < 2:
        filename += f".{_DEFAULT_DATA_FORMAT}"
        return filename, _DEFAULT_DATA_FORMAT
    try:
        extension = parts[-1]
        data_format = DataFormats(extension)
        return filename, data_format
    except ValueError:
        filename += f".{_DEFAULT_DATA_FORMAT}"
    return filename, _DEFAULT_DATA_FORMAT


@command()
@option("--count", "-c", default=_DEFAULT_CELLS_COUNT, help="number of cells")
@option("--size", "-s", default=_DEFAULT_CELL_SIZE, help="size of each cell (pixels)")
@option("--output", "-o", required=True, help="write data to file")
def main(
    count: int,
    size: int,
    output: str,
) -> None:
    filename, data_format = _check_filename(output)
    echo(f"Format: {data_format}")
    data = make_userpic(
        cells_count=count,
        cell_size=size,
        offset=size // 2,
        data_format=data_format,
    )
    path = Path(filename).resolve()
    echo(f"Save to {path}")
    with open(filename, "wb") as file:
        file.write(data)
