from dataclasses import dataclass
from enum import Enum, auto
from aoc2024.common.grid import BasicGrid, Direction, IntVector2
import aoc2024.common.input as aoc_input


class WarehouseTile(Enum):
    Wall = auto()
    Box = auto()


class Warehouse:
    grid: BasicGrid[WarehouseTile | None]
    robot_position: IntVector2

    @staticmethod
    def parse(lines: list[str]):
        char_grid = BasicGrid.parse_char_grid(lines)
        robot_position = next(pos for pos, char in char_grid.all_items() if char == "@")

        def char_to_entity(pos: IntVector2, char: str):
            match char:
                case "." | "@":
                    return None
                case "#":
                    return WarehouseTile.Wall
                case "O":
                    return WarehouseTile.Box
                case _:
                    raise AssertionError(f"unknown char at {pos}: {char}")

        grid = char_grid.map(char_to_entity)
        result = Warehouse()
        result.grid = grid
        result.robot_position = robot_position
        return result

    def format(self):
        def entity_to_char(pos: IntVector2, entity: WarehouseTile | None):
            match entity:
                case None:
                    return "."
                case WarehouseTile.Wall:
                    return "#"
                case WarehouseTile.Box:
                    return "O"

        char_grid = self.grid.map(entity_to_char)
        char_grid[self.robot_position] = "@"
        return char_grid.format_char_grid()

    def move(self, direction: Direction):
        boxes_to_push = list[IntVector2]()
        lookahead = self.robot_position + direction.to_vector()
        while self.grid[lookahead] == WarehouseTile.Box:
            boxes_to_push.append(lookahead)
            lookahead += direction.to_vector()

        if self.grid[lookahead] is None:
            for box in reversed(boxes_to_push):
                self.grid[box + direction.to_vector()] = WarehouseTile.Box
                self.grid[box] = None
            self.robot_position += direction.to_vector()

    def sum_box_gps(self):
        result = 0
        for coord, entity in self.grid.all_items():
            if entity is not WarehouseTile.Box:
                continue

            result += coord.y * 100 + coord.x
        return result


@dataclass
class PuzzleInput:
    warehouse: Warehouse
    moves: list[Direction]

    @staticmethod
    def parse(lines: list[str]):
        separator = lines.index("")
        warehouse = Warehouse.parse(lines[:separator])
        moves_str = "".join(lines[separator + 1 :])

        def parse_move(char: str):
            match (char):
                case "^":
                    return Direction.UP
                case "<":
                    return Direction.LEFT
                case ">":
                    return Direction.RIGHT
                case "v":
                    return Direction.DOWN
                case _:
                    raise AssertionError(f"unknown char: {char}")

        moves = list(map(parse_move, moves_str))

        return PuzzleInput(warehouse, moves)

    def execute(self):
        for move in self.moves:
            self.warehouse.move(move)


def part_one_answer(lines: list[str]):
    puzzle_input = PuzzleInput.parse(lines)
    puzzle_input.execute()
    return puzzle_input.warehouse.sum_box_gps()


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day15input")
    print("Part One:", part_one_answer(puzzle_input))
