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
    height: int

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
        return Schematic(schematic_type, columns, height=grid.shape.height - 1)


class PuzzleInput:
    def __init__(self, keys: list[Schematic], locks: list[Schematic]):
        self.keys = keys
        self.locks = locks
        self.height = self.keys[0].height

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

    def find_fitting_combinations(self):
        result = 0
        combinations = [(lock, key) for key in self.keys for lock in self.locks]
        for lock, key in combinations:
            valid = True
            for lock_pin_height, key_cut_height in zip(lock.columns, key.columns):
                if lock_pin_height + key_cut_height >= self.height:
                    valid = False
                    break
            if valid:
                result += 1

        return result


def part_one_answer(lines: list[str]):
    puzzle = PuzzleInput.parse(lines)
    return puzzle.find_fitting_combinations()


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day25input")
    print("Part One:", part_one_answer(puzzle_input))
