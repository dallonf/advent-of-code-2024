from collections import deque
from dataclasses import dataclass, replace
from aoc2024.common.grid import Direction, IntVector2
import aoc2024.common.input as aoc_input


class Keypad:
    def __init__(self, keys: dict[IntVector2, str]):
        self.keys = keys

    def press_button(self, coord: IntVector2) -> str:
        return self.keys[coord]

    def neighbors(self, coord: IntVector2) -> list[IntVector2]:
        return [n for n in coord.cardinal_neighbors() if n in self.keys]

    def is_in_bounds(self, coord: IntVector2) -> bool:
        return coord in self.keys


class NumericKeypad(Keypad):
    def __init__(self):
        super().__init__(
            {
                IntVector2(0, 0): "A",
                IntVector2(-1, 0): "0",
                IntVector2(-2, -1): "1",
                IntVector2(-1, -1): "2",
                IntVector2(0, -1): "3",
                IntVector2(-2, -2): "4",
                IntVector2(-1, -2): "5",
                IntVector2(0, -2): "6",
                IntVector2(-2, -3): "7",
                IntVector2(-1, -3): "8",
                IntVector2(0, -3): "9",
            }
        )


class DirectionalKeypad(Keypad):
    def __init__(self):
        super().__init__(
            {
                IntVector2(0, 0): "A",
                IntVector2(-1, 0): "^",
                IntVector2(-2, 1): "<",
                IntVector2(-1, 1): "v",
                IntVector2(0, 1): ">",
            }
        )


def key_to_direction(key: str) -> Direction | None:
    match key:
        case "^":
            return Direction.UP
        case "<":
            return Direction.LEFT
        case ">":
            return Direction.RIGHT
        case "v":
            return Direction.DOWN
        case _:
            return None


@dataclass(frozen=True)
class PathfindingNode:
    keypad_positions: tuple[IntVector2, ...]
    keys_entered: int = 0

    def input(
        self, key: str, keypads: tuple[Keypad, ...], expected_output: str
    ) -> "PathfindingNode | None":
        if len(keypads) == 0:
            if key == expected_output:
                return replace(self, keys_entered=self.keys_entered + 1)
            else:
                return None

        direction = key_to_direction(key)
        if direction is not None:
            new_position = self.keypad_positions[0] + direction.to_vector()
            if keypads[0].is_in_bounds(new_position):
                return replace(
                    self,
                    keypad_positions=(new_position,) + self.keypad_positions[1:],
                )
            else:
                return None

        if key == "A":
            result = keypads[0].press_button(self.keypad_positions[0])
            downstream = replace(
                self, keypad_positions=self.keypad_positions[1:]
            ).input(result, keypads[1:], expected_output)
            return (
                replace(
                    downstream,
                    keypad_positions=(self.keypad_positions[0],)
                    + downstream.keypad_positions,
                )
                if downstream is not None
                else None
            )

        raise AssertionError(f"Unexpected key: {key}")


def find_keypad_sequence(target_code: str, proxies: int = 1) -> int:
    keypads = tuple([DirectionalKeypad() for _ in range(proxies)] + [NumericKeypad()])
    start = PathfindingNode(tuple(IntVector2(0, 0) for _ in keypads))
    frontier = deque[PathfindingNode]([start])
    steps_so_far: dict[PathfindingNode, int] = {start: 0}

    while len(frontier) > 0:
        current = frontier.popleft()
        if current.keys_entered == len(target_code):
            return steps_so_far[current]

        next_steps = steps_so_far[current] + 1
        expected_output = target_code[current.keys_entered]
        for next_input in ("^", "<", ">", "v", "A"):
            next_node = current.input(
                next_input, keypads, expected_output=expected_output
            )
            if next_node is not None and next_node not in steps_so_far:
                frontier.append(next_node)
                steps_so_far[next_node] = next_steps

    raise AssertionError("Sequence not found")


def part_one_answer(lines: list[str]) -> int:
    result = 0
    for line in lines:
        length = find_keypad_sequence(line, proxies=2)
        numeric_code = int(line.replace("A", ""))
        result += length * numeric_code
    return result


def part_two_answer(lines: list[str]) -> int:
    result = 0
    for line in lines:
        length = find_keypad_sequence(line, proxies=25)
        numeric_code = int(line.replace("A", ""))
        result += length * numeric_code
    return result


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day21input")
    print("Part One:", part_one_answer(puzzle_input))
    # Too slow to run
    # print("Part Two:", part_two_answer(puzzle_input))
