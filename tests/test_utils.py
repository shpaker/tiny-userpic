from userpic.tools import random_bool


def test_random_bool():
    value = random_bool()

    assert isinstance(value, bool)
