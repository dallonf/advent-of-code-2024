import aoc2024.common.input as aoc_input
from .day02 import parse_reports

SAMPLE_INPUT = aoc_input.load_lines("day02sample")


def test_parse_reports():
    result = parse_reports(SAMPLE_INPUT)
    assert len(result) == 6
    assert result[0:3] == [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1]]
