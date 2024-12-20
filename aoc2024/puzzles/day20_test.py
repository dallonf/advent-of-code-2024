from pytest import skip
import aoc2024.common.input as aoc_input
from .day20 import Maze

SAMPLE_INPUT = aoc_input.load_lines("day20sample")


def test_legit_path():
    maze = Maze.parse(SAMPLE_INPUT)
    assert len(maze.get_legit_path()) == 84


def test_cheats():
    maze = Maze.parse(SAMPLE_INPUT)
    assert maze.find_cheats() == {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }


def test_minimum_savings():
    skip()
    maze = Maze.parse(SAMPLE_INPUT)
    assert maze.find_cheats(minimum_savings=20) == {
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
