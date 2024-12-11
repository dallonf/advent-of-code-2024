from .day11 import blink, multiblink


def test_blink():
    initial = [0, 1, 10, 99, 999]
    assert blink(initial) == [1, 2024, 1, 0, 9, 9, 2021976]


def test_multiblink():
    initial = [125, 17]
    assert len(multiblink(initial, 6)) == 22
    assert len(multiblink(initial, 25)) == 55312
