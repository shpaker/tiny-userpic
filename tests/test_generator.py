from userpic.userpic import make_userpic


def test_generator():
    data = make_userpic()
    assert data
