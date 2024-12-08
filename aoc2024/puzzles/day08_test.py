from textwrap import dedent
from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input
from .day08 import AntennaGrid, AntinodeType

SAMPLE_INPUT = aoc_input.load_lines("day08sample")


def test_simple_antinodes():
    expected = dedent(
        """
        ..........
        ...#......
        ..........
        ....a.....
        ..........
        .....a....
        ..........
        ......#...
        ..........
        ..........
        """
    ).strip()
    sample_input = expected.replace("#", ".")
    grid = AntennaGrid.parse(aoc_input.lines(sample_input))
    assert grid.antinodes == {("a", IntVector2(3, 1)), ("a", IntVector2(6, 7))}
    assert grid.debug_antinodes() == expected


def test_multiple_antennas():
    expected = dedent(
        """
        ..........
        ...#......
        #.........
        ....a.....
        ........a.
        .....a....
        ..#.......
        ......#...
        ..........
        ..........
        """
    ).strip()
    sample_input = expected.replace("#", ".")
    grid = AntennaGrid.parse(aoc_input.lines(sample_input))
    assert grid.debug_antinodes() == expected


def test_complex():
    expected = dedent(
        """
        ......#....#
        ...#....0...
        ....#0....#.
        ..#....0....
        ....0....#..
        .#....A.....
        ...#........
        #......#....
        ........A...
        .........A..
        ..........#.
        ..........#.
        """
    ).strip()
    sample_input = expected.replace("#", ".")
    grid = AntennaGrid.parse(aoc_input.lines(sample_input))
    assert grid.debug_antinodes() == expected


def test_part_one_answer():
    grid = AntennaGrid.parse(SAMPLE_INPUT)
    assert grid.part_one_answer() == 14


def test_resonant_antinodes():
    expected = dedent(
        """
        ##....#....#
        .#.#....0...
        ..#.#0....#.
        ..##...0....
        ....0....#..
        .#...#A....#
        ...#..#.....
        #....#.#....
        ..#.....A...
        ....#....A..
        .#........#.
        ...#......##
        """
    ).strip()
    sample_input = expected.replace("#", ".")
    grid = AntennaGrid.parse(aoc_input.lines(sample_input))
    assert grid.debug_antinodes(type=AntinodeType.Resonant) == expected
