from .day22 import mix, prune, next_secret, part_one_answer


def test_mix():
    assert mix(15, 42) == 37


def test_prune():
    assert prune(100_000_000) == 16_113_920


def test_next_secret():
    assert next_secret(123) == 15887950
    assert next_secret(15887950) == 16495136


def test_part_one_answer():
    sample_input = [
        "1",
        "10",
        "100",
        "2024",
    ]
    assert part_one_answer(sample_input) == 37327623
