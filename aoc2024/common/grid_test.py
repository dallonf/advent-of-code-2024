from textwrap import dedent
import aoc2024.common.input as aoc_input
from aoc2024.common.grid import BasicGrid


class TestBasicGrid:
    def test_parse(self):
        test_input = dedent(
            """
            MMMSXXMASM
            MSAMXMSMSA
            AMXSXMAAMM
            MSAMASMSMX
            XMASAMXAMM
            XXAMMXXAMA
            SMSMSASXSS
            SAXAMASAAA
            MAMMMXMMMM
            MXMXAXMASX
            """
        )
        test_input = aoc_input.lines(test_input)
        grid = BasicGrid.parse_char_grid(test_input)
        assert grid.shape.width == 10
        assert grid.shape.height == 10
        assert grid.format_char_grid().splitlines() == test_input
