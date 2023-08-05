"""Simple test."""


from tuyau import Tube


def add_one(number: int) -> int:
    """Simple steps, add one to number."""
    return number + 1


def test_simple_return() -> None:
    """Test sending values through the Tuyau. and get result."""
    _number = 42
    assert Tube(str, int)(_number) == _number  # noqa: S101


def test_simple_send() -> None:
    """Test sending values through the Tuyau. with .send."""
    _ret: list[int] = []
    tuyau: Tube[int, None] = Tube(*[add_one] * 100, lambda v: _ret.append(v))
    for i in range(1, 4):
        tuyau.send(i)

    assert _ret == [101, 102, 103]  # noqa: S101


def test_simple_call() -> None:
    """Test calling the Tuyau directly with values. call directly."""
    _ret: list[int] = []

    tuyau: Tube[int, None] = Tube(*[add_one] * 100, lambda v: _ret.append(v))
    for i in range(1, 4):
        tuyau(i)

    assert _ret == [101, 102, 103]  # noqa: S101
