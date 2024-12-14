from textwrap import dedent
from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input
from aoc2024.puzzles.day14 import (
    Robot,
    count_by_quadrant,
    debug_robot_counts,
    sample_shape,
    part_one_answer,
)

SAMPLE_INPUT = aoc_input.load_lines("day14sample")


def test_robot_parse():
    robot = Robot.parse("p=0,4 v=3,-3")
    assert robot == Robot(IntVector2(0, 4), IntVector2(3, -3))


def test_robot_move():
    robot = Robot.parse("p=2,4 v=2,-3")
    shape = sample_shape()
    robot.move(shape)
    assert robot.position == IntVector2(4, 1)
    robot.move(shape)
    assert robot.position == IntVector2(6, 5)  # wraps from top to bottom
    robot.move(shape)
    assert robot.position == IntVector2(8, 2)
    robot.move(shape)
    assert robot.position == IntVector2(10, 6)  # wraps from top to bottom again
    robot.move(shape)
    assert robot.position == IntVector2(1, 3)  # wraps from right to left


def test_robot_move_multiple():
    robot = Robot.parse("p=2,4 v=2,-3")
    shape = sample_shape()
    robot.move(shape, times=5)
    assert robot.position == IntVector2(1, 3)


def test_count_by_quadrant():
    robots = Robot.parse_all(SAMPLE_INPUT)
    shape = sample_shape()
    for r in robots:
        r.move(shape, 100)
    assert count_by_quadrant(robots, shape) == (1, 3, 4, 1)


def test_format():
    robots = Robot.parse_all(SAMPLE_INPUT)
    shape = sample_shape()
    expected = dedent(
        """
        1.12.......
        ...........
        ...........
        ......11.11
        1.1........
        .........1.
        .......1...
        """
    ).strip()
    assert debug_robot_counts(robots, shape) == expected


def test_counts_after_movement():
    robots = Robot.parse_all(SAMPLE_INPUT)
    shape = sample_shape()
    for r in robots:
        r.move(shape, 100)
    expected = dedent(
        """
        ......2..1.
        ...........
        1..........
        .11........
        .....1.....
        ...12......
        .1....1....
        """
    ).strip()
    assert debug_robot_counts(robots, shape) == expected


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT, sample_shape()) == 12
