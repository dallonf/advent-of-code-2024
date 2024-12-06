from aoc2024.common.grid import Direction, GridShape, IntVector2
from .day06 import GuardMap, PathResultType
import aoc2024.common.input as aoc_input

SAMPLE_INPUT = aoc_input.load_lines("day06sample")


def test_parse():
    result = GuardMap.parse(SAMPLE_INPUT)
    assert result.shape == GridShape(10, 10)
    assert len(result.obstacles) == 8
    assert result.starting_position == IntVector2(4, 6)


def test_covered_positions():
    guard_map = GuardMap.parse(SAMPLE_INPUT)
    result = guard_map.get_covered_positions()
    assert len(result) == 41


def test_path_result():
    guard_map = GuardMap.parse(SAMPLE_INPUT)
    path_result = guard_map.get_path()
    assert path_result.type == PathResultType.EXITED

    obstacle = guard_map.starting_position + Direction.LEFT.to_vector()
    map_with_obstacle: GuardMap = guard_map.with_new_obstacle(obstacle)
    path_result = map_with_obstacle.get_path()
    assert path_result.type == PathResultType.LOOPING


def test_possible_looping_obstructions():
    guard_map = GuardMap.parse(SAMPLE_INPUT)
    result = guard_map.get_possible_looping_obstructions()
    assert len(result) == 6
