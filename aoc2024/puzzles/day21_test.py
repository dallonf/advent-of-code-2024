from .day21 import find_keypad_sequence, part_one_answer


def test_find_single_keypad_sequence():
    assert find_keypad_sequence("029A", proxies=0) == 12


def test_proxy_keypad():
    assert find_keypad_sequence("029A", proxies=1) == 28


def test_double_proxy():
    assert find_keypad_sequence("029A", proxies=2) == 68


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
