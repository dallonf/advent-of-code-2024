from textwrap import dedent
import aoc2024.common.input as aoc_input
from .day18 import Region, parse_obstacles, part_one_answer, sample_shape

SAMPLE_INPUT = aoc_input.load_lines("day18sample")


def test_parse_and_add_obstacles():
    obstacles = parse_obstacles(SAMPLE_INPUT)
    region = Region(sample_shape())
    region.add_obstacles(obstacles[:12])
    format = region.debug()
    assert (
        format
        == dedent(
            """
            ...#...
            ..#..#.
            ....#..
            ...#..#
            ..#..#.
            .#..#..
            #.#....
            """
        ).strip()
    )


def test_part_one_answer():
    result = part_one_answer(SAMPLE_INPUT, shape=sample_shape(), falling_ticks=12)
    assert result == 22
