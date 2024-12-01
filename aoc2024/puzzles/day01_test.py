from textwrap import dedent
from aoc2024.puzzles.day01 import parse_lists


SAMPLE_INPUT = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def test_parse_lists():
    result = parse_lists(SAMPLE_INPUT)
    assert result[0] == [3, 4, 2, 1, 3, 3]
    assert result[1] == [4, 3, 5, 3, 9, 3]


def test_parse_lists_longer_numbers():
    input = dedent(
        """\
    123   456
    789   101
    """
    )
    result = parse_lists(input)
    assert result[0] == [123, 789]
    assert result[1] == [456, 101]
