from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from aoc2024.common.grid import BasicGrid, Direction, GridShape, IntVector2
import aoc2024.common.input as aoc_input


@dataclass(frozen=True)
class WideBox:
    left: IntVector2

    @property
    def right(self):
        return self.left + Direction.RIGHT.to_vector()


class WarehouseTile(Enum):
    Wall = auto()
    Box = auto()
    WideBoxLeft = auto()
    WideBoxRight = auto()


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
                # parse these for testing
                case "[":
                    return WarehouseTile.WideBoxLeft
                case "]":
                    return WarehouseTile.WideBoxRight
                case _:
                    raise AssertionError(f"unknown char at {pos}: {char}")

        grid = char_grid.map(char_to_entity)
        result = Warehouse()
        result.grid = grid
        result.robot_position = robot_position
        return result

    @staticmethod
    def parse_wide(lines: list[str]):
        char_grid = BasicGrid.parse_char_grid(lines)
        robot_position = next(pos for pos, char in char_grid.all_items() if char == "@")
        robot_position += IntVector2(robot_position.x, 0)

        grid = BasicGrid[WarehouseTile | None].filled(
            GridShape(char_grid.width * 2, char_grid.shape.height), None
        )

        for thin_pos, char in char_grid.all_items():
            pos_left = thin_pos + IntVector2(thin_pos.x, 0)
            pos_right = pos_left + Direction.RIGHT.to_vector()
            match char:
                case "." | "@":
                    pass
                case "#":
                    grid[pos_left] = WarehouseTile.Wall
                    grid[pos_right] = WarehouseTile.Wall
                case "O":
                    grid[pos_left] = WarehouseTile.WideBoxLeft
                    grid[pos_right] = WarehouseTile.WideBoxRight
                case _:
                    raise AssertionError(f"unknown char at {thin_pos}: {char}")

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
                case WarehouseTile.WideBoxLeft:
                    return "["
                case WarehouseTile.WideBoxRight:
                    return "]"

        char_grid = self.grid.map(entity_to_char)
        char_grid[self.robot_position] = "@"
        return char_grid.format_char_grid()

    def move(self, direction: Direction):
        is_horizontal = direction in (Direction.LEFT, Direction.RIGHT)
        boxes_to_push = list[IntVector2 | WideBox]()
        lookahead_queue = deque([self.robot_position + direction.to_vector()])
        while len(lookahead_queue) > 0:
            tile = self.grid[(lookahead := lookahead_queue.popleft())]
            match tile:
                case WarehouseTile.Box:
                    boxes_to_push.append(lookahead)
                    lookahead_queue.append(lookahead + direction.to_vector())
                case WarehouseTile.WideBoxLeft | WarehouseTile.WideBoxRight:
                    wide_box = (
                        WideBox(lookahead)
                        if tile == WarehouseTile.WideBoxLeft
                        else WideBox(lookahead + Direction.LEFT.to_vector())
                    )
                    if wide_box in boxes_to_push:
                        continue
                    boxes_to_push.append(wide_box)
                    if is_horizontal:
                        lookahead_queue.append(lookahead + direction.to_vector() * 2)
                    else:
                        lookahead_queue.append(wide_box.left + direction.to_vector())
                        lookahead_queue.append(wide_box.right + direction.to_vector())
                case WarehouseTile.Wall:
                    return
                case None:
                    break

        for box in reversed(boxes_to_push):
            if isinstance(box, WideBox):
                self.grid[box.left] = None
                self.grid[box.right] = None
                self.grid[box.left + direction.to_vector()] = WarehouseTile.WideBoxLeft
                self.grid[box.right + direction.to_vector()] = (
                    WarehouseTile.WideBoxRight
                )
            else:
                self.grid[box + direction.to_vector()] = WarehouseTile.Box
                self.grid[box] = None
        self.robot_position += direction.to_vector()

    def sum_box_gps(self):
        result = 0
        for coord, entity in self.grid.all_items():
            if entity not in (WarehouseTile.Box, WarehouseTile.WideBoxLeft):
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
        moves = parse_moves(lines[separator + 1 :])

        return PuzzleInput(warehouse, moves)

    @staticmethod
    def parse_wide(lines: list[str]):
        separator = lines.index("")
        warehouse = Warehouse.parse_wide(lines[:separator])
        moves = parse_moves(lines[separator + 1 :])

        return PuzzleInput(warehouse, moves)

    def execute(self):
        for move in self.moves:
            self.warehouse.move(move)


def parse_moves(lines: list[str]):
    moves_str = "".join(lines)

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

    return list(map(parse_move, moves_str))


def part_one_answer(lines: list[str]):
    puzzle_input = PuzzleInput.parse(lines)
    puzzle_input.execute()
    return puzzle_input.warehouse.sum_box_gps()


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day15input")
    print("Part One:", part_one_answer(puzzle_input))
