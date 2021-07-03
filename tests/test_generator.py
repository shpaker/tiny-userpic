from userpic import make_userpic
from magic import Magic

magic = Magic(mime=True, uncompress=True)


def test_generator_png() -> None:
    data = make_userpic(data_format="png")
    mime = magic.from_buffer(data)
    assert mime == "image/png"


def test_generator_svg() -> None:
    data = make_userpic(data_format="svg")
    mime = magic.from_buffer(data)
    assert mime == "image/svg+xml"
