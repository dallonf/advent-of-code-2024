from aoc2024.common.grid import GridShape, IntVector
from .day06 import GuardMap
import aoc2024.common.input as aoc_input

SAMPLE_INPUT = aoc_input.load_lines("day06sample")


def test_parse():
    result = GuardMap.parse(SAMPLE_INPUT)
    assert result.shape == GridShape(10, 10)
    assert len(result.obstacles) == 8
    assert result.starting_position == IntVector(4, 6)


def test_covered_positions():
    guard_map = GuardMap.parse(SAMPLE_INPUT)
    result = guard_map.get_covered_positions()
    assert len(result) == 41
