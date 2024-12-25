from dataclasses import dataclass
from enum import Enum, auto
from aoc2024.common.grid import BasicGrid
import aoc2024.common.input as aoc_input


class SchematicType(Enum):
    Lock = auto()
    Key = auto()


@dataclass(frozen=True)
class Schematic:
    type: SchematicType
    columns: list[int]

    @staticmethod
    def parse(lines: list[str]):
        grid = BasicGrid.parse_char_grid(lines)
        bottom_y = grid.shape.height - 1
        if all(grid[x, 0] == "#" for x in range(grid.shape.width)):
            schematic_type = SchematicType.Lock
        elif all(grid[x, bottom_y] == "#" for x in range(grid.shape.width)):
            schematic_type = SchematicType.Key
        else:
            raise AssertionError("Neither a lock or a key")

        columns = list[int]()
        for x in range(grid.shape.width):
            columns.append(
                # subtract 1 so that we don't count the filled row
                sum(1 for y in range(grid.shape.height) if grid[x, y] == "#")
                - 1
            )
        return Schematic(schematic_type, columns)


class PuzzleInput:
    def __init__(self, keys: list[Schematic], locks: list[Schematic]):
        self.keys = keys
        self.locks = locks

    @staticmethod
    def parse(lines: list[str]):
        schematics = list[Schematic]()
        lines.append("")  # end with a blank line to simplify separation
        line_idx = 0
        while line_idx < len(lines) - 1:
            next_split = lines.index("", line_idx)
            schematics.append(Schematic.parse(lines[line_idx:next_split]))
            line_idx = next_split + 1
        return PuzzleInput(
            keys=[s for s in schematics if s.type == SchematicType.Key],
            locks=[s for s in schematics if s.type == SchematicType.Lock],
        )


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day25input")
