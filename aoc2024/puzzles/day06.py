from dataclasses import dataclass
from aoc2024.common.grid import BasicGrid, Direction, GridShape, IntVector2
import aoc2024.common.input as aoc_input


@dataclass
class GuardMap:
    shape: GridShape
    obstacles: set[IntVector2]
    starting_position: IntVector2

    @staticmethod
    def parse(lines: list[str]):
        basic = BasicGrid.parse_char_grid(lines)
        obstacles = set[IntVector2]()
        starting_position = None
        for coord, entry in basic.all_items():
            if entry == "#":
                obstacles.add(coord)
            elif entry == "^":
                starting_position = coord
        assert starting_position != None
        return GuardMap(
            shape=basic.shape, obstacles=obstacles, starting_position=starting_position
        )

    def get_covered_positions(self):
        result = set[IntVector2]()
        direction = Direction.UP
        position = self.starting_position

        while self.shape.is_in_bounds(position):
            result.add(position)
            next_position = position + direction.to_vector()
            if next_position in self.obstacles:
                direction = direction.clockwise()
            else:
                position = next_position

        return result

    def part_one_result(self):
        return len(self.get_covered_positions())


if __name__ == "__main__":
    puzzle_input = GuardMap.parse(aoc_input.load_lines("day06input"))
    print("Part One", puzzle_input.part_one_result())
