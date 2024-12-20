from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input
from .day20 import Maze, get_surrounding

SAMPLE_INPUT = aoc_input.load_lines("day20sample")


def test_legit_path():
    maze = Maze.parse(SAMPLE_INPUT)
    assert len(maze.get_legit_path()) == 84


def test_get_surrounding():
    result = get_surrounding(IntVector2(0, 0), 1)
    assert result == set(
        [
            IntVector2(0, 1),
            IntVector2(x=1, y=0),
            IntVector2(x=-1, y=0),
            IntVector2(x=0, y=-1),
        ]
    )


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
    maze = Maze.parse(SAMPLE_INPUT)
    assert maze.find_cheats(minimum_savings=20) == {
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }


def test_long_cheats():
    maze = Maze.parse(SAMPLE_INPUT)

    assert maze.find_cheats(cheat_length=20, minimum_savings=50) == {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }
