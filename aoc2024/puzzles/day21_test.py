from aoc2024.common.grid import IntVector2
from .day21 import (
    find_keypad_sequence,
    part_one_answer,
    steps_to_press_button,
    numeric_keypad,
)


def test_find_single_keypad_sequence():
    assert find_keypad_sequence("029A", proxies=0) == 12


def test_proxy_keypad():
    assert find_keypad_sequence("029A", proxies=1) == 28


def test_double_proxy():
    assert find_keypad_sequence("029A", proxies=2) == 68


def test_others():
    assert find_keypad_sequence("980A", proxies=2) == 60
    assert find_keypad_sequence("179A", proxies=2) == 68
    assert find_keypad_sequence("456A", proxies=2) == 64

    assert find_keypad_sequence("379A", proxies=0) == 14
    assert find_keypad_sequence("379A", proxies=1) == 28
    assert find_keypad_sequence("379A", proxies=2) == 64


def test_part_one_answer():
    assert (
        part_one_answer(
            [
                "029A",
                "980A",
                "179A",
                "456A",
                "379A",
            ]
        )
        == 126384
    )


def test_steps_to_press_button_no_proxies():
    assert (
        steps_to_press_button(
            "0",
            keypad=numeric_keypad,
            current_position=IntVector2(0, 0),
            directional_keypads_above=1,
        )
        == 2
    )
    assert (
        steps_to_press_button(
            "2",
            keypad=numeric_keypad,
            current_position=IntVector2(-1, 0),
            directional_keypads_above=1,
        )
        == 2
    )
    assert (
        steps_to_press_button(
            "9",
            keypad=numeric_keypad,
            current_position=IntVector2(-1, -1),
            directional_keypads_above=1,
        )
        == 4
    )
    assert (
        steps_to_press_button(
            "A",
            keypad=numeric_keypad,
            current_position=IntVector2(0, -3),
            directional_keypads_above=1,
        )
        == 4
    )
