import aoc2024.common.input as aoc_input
from .day25 import PuzzleInput

SAMPLE_INPUT = aoc_input.load_lines("day25sample")


def test_parse():
    puzzle = PuzzleInput.parse(SAMPLE_INPUT)
    assert len(puzzle.locks) == 2
    assert len(puzzle.keys) == 3
    assert puzzle.locks[0].columns == [0, 5, 3, 4, 3]
