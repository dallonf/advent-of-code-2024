import aoc2024.common.input as aoc_input
from .day02 import (
    parse_reports,
    parse_report,
    is_safe,
    part_one_answer,
    is_safe_with_dampener,
    part_two_answer,
)

SAMPLE_INPUT = aoc_input.load_lines("day02sample")


def test_parse_reports():
    result = parse_reports(SAMPLE_INPUT)
    assert len(result) == 6
    assert result[0:3] == [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1]]


def test_is_safe():
    def is_safe_parsed(line: str) -> bool:
        return is_safe(parse_report(line))

    assert is_safe_parsed("7 6 4 2 1") == True
    assert is_safe_parsed("1 2 7 8 9") == False
    assert is_safe_parsed("9 7 6 2 1") == False
    assert is_safe_parsed("1 3 2 4 5") == False
    assert is_safe_parsed("8 6 4 4 1") == False
    assert is_safe_parsed("1 3 6 7 9") == True


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT) == 2


def test_is_safe_with_dampener():
    def is_safe_parsed(line: str) -> bool:
        return is_safe_with_dampener(parse_report(line))

    assert is_safe_parsed("7 6 4 2 1") == True
    assert is_safe_parsed("1 2 7 8 9") == False
    assert is_safe_parsed("9 7 6 2 1") == False
    assert is_safe_parsed("1 3 2 4 5") == True
    assert is_safe_parsed("8 6 4 4 1") == True
    assert is_safe_parsed("1 3 6 7 9") == True


def test_part_two_answer():
    assert part_two_answer(SAMPLE_INPUT) == 4
