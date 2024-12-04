from dataclasses import dataclass
from aoc2024.common.grid import BasicGrid, IntVector
import aoc2024.common.input as aoc_input


@dataclass
class FoundXmas:
    "coord is the coordinate of the X letter"
    coord: IntVector
    direction: IntVector


def find_xmases(grid: BasicGrid[str]) -> list[FoundXmas]:
    result: list[FoundXmas] = []
    for coord in grid.shape.all_coords():
        if grid[coord] == "X":
            for direction in IntVector.eight_directions():
                if (
                    grid.get_if_in_bounds(coord + direction) == "M"
                    and grid.get_if_in_bounds(coord + direction * 2) == "A"
                    and grid.get_if_in_bounds(coord + direction * 3) == "S"
                ):
                    result.append(FoundXmas(coord, direction))
    return result


def part_one_answer(lines: list[str]) -> int:
    grid = BasicGrid.parse_char_grid(lines)
    xmases = find_xmases(grid)
    return len(xmases)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day04input")
    print("Part One:", part_one_answer(puzzle_input))
