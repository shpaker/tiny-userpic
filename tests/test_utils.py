from userpic.utils import random_bool


def test_random_bool() -> None:
    value = random_bool()
    assert isinstance(value, bool)
