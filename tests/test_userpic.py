from pytest import mark, param
from userpic import make_userpic

_MAGIC_DOESNT_EXIST_ERROR = None

try:
    from magic import Magic
except ImportError as err:
    _MAGIC_DOESNT_EXIST_ERROR = str(err)


@mark.parametrize(
    ("data_format", "expected_mime"),
    (
        param("svg", "image/svg+xml"),
        param("png", "image/png"),
    ),
)
@mark.skipif(
    _MAGIC_DOESNT_EXIST_ERROR is not None,
    reason=_MAGIC_DOESNT_EXIST_ERROR or "",
)
def test_ok(
    data_format: str,
    expected_mime: str,
) -> None:
    magic = Magic(mime=True, uncompress=True)
    data = make_userpic(data_format=data_format)
    mime = magic.from_buffer(data)
    assert mime == expected_mime
