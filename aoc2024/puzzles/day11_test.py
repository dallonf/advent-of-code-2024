from .day11 import blink, count_after_blinks


def test_blink():
    initial = (0, 1, 10, 99, 999)
    assert blink(initial) == (1, 2024, 1, 0, 9, 9, 2021976)


def test_count_after_blinks():
    initial = (125, 17)
    assert count_after_blinks(initial, 6) == 22
    assert count_after_blinks(initial, 25) == 55312
