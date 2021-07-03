from typing import Tuple

from typer import run
from userpic import make_userpic, DataFormats

DEFAULT_DATA_FORMAT = DataFormats.PNG
DEFAULT_FILENAME = "output.png"


def check_filename(filename: str) -> Tuple[str, DataFormats]:
    parts = filename.split(".")
    if len(parts) < 2:
        filename += f".{DEFAULT_DATA_FORMAT}"
        return filename, DEFAULT_DATA_FORMAT
    try:
        extension = parts[-1]
        data_format = DataFormats(extension)
        return filename, data_format
    except ValueError:
        filename += f".{DEFAULT_DATA_FORMAT}"
    return filename, DEFAULT_DATA_FORMAT


def main(
    count: int = 9,
    size: int = 16,
    output: str = DEFAULT_FILENAME,
) -> None:
    filename, data_format = check_filename(output)
    data = make_userpic(
        cells_count=count,
        cell_size=size,
        offset=size//2,
        data_format=data_format,
    )
    with open(filename, "wb") as file:
        file.write(data)


if __name__ == "__main__":
    run(main)
