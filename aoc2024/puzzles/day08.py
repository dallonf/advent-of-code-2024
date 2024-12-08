from dataclasses import dataclass
from functools import cached_property
import itertools
from aoc2024.common.grid import BasicGrid, IntVector2
import aoc2024.common.input as aoc_input


@dataclass
class AntennaGrid:
    grid: BasicGrid[str]

    @staticmethod
    def parse(lines: list[str]) -> "AntennaGrid":
        grid = BasicGrid.parse_char_grid(lines)
        return AntennaGrid(grid)

    @cached_property
    def groups(self) -> list["AntennaGroup"]:
        found = dict[str, set[IntVector2]]()
        for pos, tile in self.grid.all_items():
            if tile.isalnum():
                antennas = found.setdefault(tile, set())
                antennas.add(pos)

        return [AntennaGroup(key, antennas) for key, antennas in found.items()]

    @cached_property
    def antinodes(self) -> set[tuple[str, IntVector2]]:
        result = set[tuple[str, IntVector2]]()
        for g in self.groups:

            def add_if_in_bounds(pos: IntVector2):
                if self.grid.shape.is_in_bounds(pos):
                    result.add((g.key, pos))

            pairs = itertools.combinations(g.antennas, 2)
            for a, b in pairs:
                delta = a - b
                add_if_in_bounds(a + delta)
                add_if_in_bounds(b - delta)

        return result

    @cached_property
    def unique_antinode_positions(self) -> set[IntVector2]:
        return {pos for _, pos in self.antinodes}

    def part_one_answer(self):
        return len(self.unique_antinode_positions)

    def debug_antinodes(self) -> str:
        """
        if an antenna and an antinode appear in the same position,
        the antenna is rendered and the antinode is hidden.
        """

        def map_to_debug(pos: IntVector2, char: str):
            if char == "." and pos in self.unique_antinode_positions:
                return "#"
            else:
                return char

        debug_grid = self.grid.map(map_to_debug)
        return debug_grid.format_char_grid()


@dataclass
class AntennaGroup:
    key: str
    antennas: set[IntVector2]


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day08input")
    grid = AntennaGrid.parse(puzzle_input)
    print("Part One:", grid.part_one_answer())
