from textwrap import dedent
from aoc2024.common.grid import BasicGrid, IntVector
import aoc2024.common.input as aoc_input
from .day04 import find_xmases, part_one_answer

SAMPLE_INPUT = aoc_input.load_lines("day04sample")
SAMPLE_GRID = BasicGrid.parse_char_grid(SAMPLE_INPUT)


def test_find_xmases_count():
    xmases = find_xmases(SAMPLE_GRID)
    assert len(xmases) == 18


def test_find_xmases_grid():
    affected_coords = set[IntVector]()
    xmases = find_xmases(SAMPLE_GRID)
    for xmas in xmases:
        for i in range(4):
            affected_coords.add(xmas.coord + xmas.direction * i)

    debug_grid = SAMPLE_GRID.copy()
    for coord in debug_grid.shape.all_coords():
        if coord not in affected_coords:
            debug_grid[coord] = "."

    expected_output = dedent(
        """
            ....XXMAS.
            .SAMXMS...
            ...S..A...
            ..A.A.MS.X
            XMASAMX.MM
            X.....XA.A
            S.S.S.S.SS
            .A.A.A.A.A
            ..M.M.M.MM
            .X.X.XMASX
        """
    ).strip()
    assert debug_grid.format_char_grid() == expected_output


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT) == 18
