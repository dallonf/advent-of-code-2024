from dataclasses import dataclass
from typing import cast
from aoc2024.common.grid import BasicGrid, IntVector2
import aoc2024.common.input as aoc_input


@dataclass
class FoundXmas:
    "coord is the coordinate of the X letter"
    coord: IntVector2
    direction: IntVector2


def find_xmases(grid: BasicGrid[str]) -> list[FoundXmas]:
    result: list[FoundXmas] = []
    for coord in grid.shape.all_coords():
        # from any X, check for a "MAS" extending in any direction
        if grid[coord] == "X":
            for direction in IntVector2.eight_directions():
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


def find_cross_mases(grid: BasicGrid[str]) -> list[IntVector2]:
    result: list[IntVector2] = []
    for coord in grid.shape.all_coords():
        if grid[coord] == "A":
            # we're expecting both diagnonals to form a MAS, forward or backward.
            diagonals = [
                [
                    grid.get_if_in_bounds(coord + IntVector2(-1, -1)),
                    grid.get_if_in_bounds(coord + IntVector2(1, 1)),
                ],
                [
                    grid.get_if_in_bounds(coord + IntVector2(1, -1)),
                    grid.get_if_in_bounds(coord + IntVector2(-1, 1)),
                ],
            ]

            # make sure none of the elements are out of bounds
            if any((letter == None for line in diagonals for letter in line)):
                continue
            diagonals = cast(list[list[int]], diagonals)

            # We can just check for MS after sorting
            for d in diagonals:
                d.sort()
            if diagonals == [["M", "S"], ["M", "S"]]:
                result.append(coord)
    return result


def part_two_answer(lines: list[str]) -> int:
    grid = BasicGrid.parse_char_grid(lines)
    results = find_cross_mases(grid)
    return len(results)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day04input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
