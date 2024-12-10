from textwrap import dedent
from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input
from .day10 import TopoMap, part_one_answer, part_two_answer

SAMPLE_INPUT = aoc_input.load_lines("day10sample")


def test_trailhead():
    sample_input = aoc_input.lines(
        dedent(
            """
            ...0...
            ...1...
            ...2...
            6543456
            7.....7
            8.....8
            9.....9
            """
        )
    )
    topomap = TopoMap.parse(sample_input)
    assert topomap.score_trailhead(IntVector2(3, 0)) == 2

    sample_input = aoc_input.lines(
        dedent(
            """
            ..90..9
            ...1.98
            ...2..7
            6543456
            765.987
            876....
            987....
            """
        )
    )
    topomap = TopoMap.parse(sample_input)
    assert topomap.score_trailhead(IntVector2(3, 0)) == 4


def test_score_all_trailheads():
    sample_input = aoc_input.lines(
        dedent(
            """
            10..9..
            2...8..
            3...7..
            4567654
            ...8..3
            ...9..2
            .....01
            """
        )
    )
    topomap = TopoMap.parse(sample_input)
    assert set(topomap.score_all_trailheads()) == set(
        ((IntVector2(1, 0), 1), (IntVector2(5, 6), 2))
    )


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT) == 36


def test_trailhead_rating():
    sample_input = aoc_input.lines(
        dedent(
            """
            .....0.
            ..4321.
            ..5..2.
            ..6543.
            ..7..4.
            ..8765.
            ..9....
            """
        )
    )
    topomap = TopoMap.parse(sample_input)
    assert topomap.get_rating(IntVector2(5, 0)) == 3

    sample_input = aoc_input.lines(
        dedent(
            """
            ..90..9
            ...1.98
            ...2..7
            6543456
            765.987
            876....
            987....

            """
        )
    )
    topomap = TopoMap.parse(sample_input)
    assert topomap.get_rating(IntVector2(3, 0)) == 13


def test_part_two_answer():
    assert part_two_answer(SAMPLE_INPUT) == 81
