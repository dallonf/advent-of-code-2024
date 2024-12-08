from dataclasses import dataclass
from enum import Enum, auto
from fractions import Fraction
from functools import cached_property
import itertools
from aoc2024.common.grid import BasicGrid, IntVector2
import aoc2024.common.input as aoc_input


class AntinodeType(Enum):
    Simple = auto()
    Resonant = auto()


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

    @cached_property
    def unique_resonant_antinode_positions(self) -> set[IntVector2]:
        result = set[IntVector2]()
        for g in self.groups:
            pairs = itertools.combinations(g.antennas, 2)
            for a, b in pairs:
                delta = a - b
                # simplifying the delta doesn't actually seem to be necessary...?
                # in the data provided, there don't appear to be any antennas with an antinode between them
                # keeping the computation for posterity, though
                fraction = Fraction(delta.x, delta.y)
                simplified_delta = IntVector2(fraction.numerator, fraction.denominator)
                candidate = a
                # loop forwards and backwards until you go out of bounds
                while self.grid.shape.is_in_bounds(candidate):
                    result.add(candidate)
                    candidate += simplified_delta
                candidate = a - simplified_delta
                while self.grid.shape.is_in_bounds(candidate):
                    result.add(candidate)
                    candidate -= simplified_delta
        return result

    def get_unique_antinode_positions(self, type: AntinodeType = AntinodeType.Simple):
        match type:
            case AntinodeType.Simple:
                return self.unique_antinode_positions
            case AntinodeType.Resonant:
                return self.unique_resonant_antinode_positions

    def part_one_answer(self):
        return len(self.unique_antinode_positions)
    
    def part_two_answer(self):
        return len(self.unique_resonant_antinode_positions)

    def debug_antinodes(self, type: AntinodeType = AntinodeType.Simple) -> str:
        """
        if an antenna and an antinode appear in the same position,
        the antenna is rendered and the antinode is hidden.
        """

        def map_to_debug(pos: IntVector2, char: str):
            if char == "." and pos in self.get_unique_antinode_positions(type):
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
    print("Part Two:", grid.part_two_answer())
