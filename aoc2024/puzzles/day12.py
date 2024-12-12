from collections import deque
from dataclasses import dataclass
from functools import cached_property
from aoc2024.common.grid import BasicGrid, IntVector2
import aoc2024.common.input as aoc_input


@dataclass(eq=True, frozen=True)
class Region:
    plant: str
    coords: frozenset[IntVector2]

    @cached_property
    def perimeter(self) -> int:
        result = 0
        for coord in self.coords:
            for neighbor in coord.cardinal_neighbors():
                if neighbor not in self.coords:
                    result += 1
        return result

    @cached_property
    def price_to_fence(self) -> int:
        return len(self.coords) * self.perimeter


class RegionSolver:
    def __init__(self, grid: BasicGrid[str]):
        self.grid = grid
        self.discovered = dict[IntVector2, Region]()

    def get_regions(self) -> set[Region]:
        for coord in self.grid.shape.all_coords():
            self.discover(coord)
        return set(self.discovered.values())

    def discover(self, coord: IntVector2):
        if coord in self.discovered:
            return

        plant = self.grid[coord]
        queue = deque([coord])
        found = set[IntVector2]()
        while len(queue) > 0:
            exploring = queue.popleft()

            if self.grid.get_if_in_bounds(exploring) != plant:
                continue

            if exploring in found:
                continue
            found.add(exploring)

            queue.extend(exploring.cardinal_neighbors())

        region = Region(plant, frozenset(found))
        for region_coord in found:
            self.discovered[region_coord] = region


def parse(lines: list[str]):
    return BasicGrid.parse_char_grid(lines)


def get_regions(grid: BasicGrid[str]):
    solver = RegionSolver(grid)
    return solver.get_regions()


def part_one_answer(lines: list[str]) -> int:
    regions = get_regions(parse(lines))
    return sum(r.price_to_fence for r in regions)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day12input")
    print("Part One:", part_one_answer(puzzle_input))
