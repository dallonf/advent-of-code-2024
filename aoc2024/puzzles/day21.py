from collections import deque
from dataclasses import dataclass, replace
from functools import cached_property
from aoc2024.common.grid import Direction, IntVector2
import aoc2024.common.input as aoc_input
from aoc2024.common.priority_queue import PriorityQueue


class Keypad:
    def __init__(self, name: str, keys: dict[IntVector2, str]):
        self.keys = keys
        self.name = name

    def __str__(self):
        return f"keypad: {self.name}"

    @cached_property
    def key_positions(self):
        return {v: k for k, v in self.keys.items()}

    def press_button(self, coord: IntVector2) -> str:
        return self.keys[coord]

    def neighbors(self, coord: IntVector2) -> list[IntVector2]:
        return [n for n in coord.cardinal_neighbors() if n in self.keys]

    def is_in_bounds(self, coord: IntVector2) -> bool:
        return coord in self.keys


numeric_keypad = Keypad(
    "numeric",
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
    },
)


directional_keypad = Keypad(
    "directional",
    {
        IntVector2(0, 0): "A",
        IntVector2(-1, 0): "^",
        IntVector2(-2, 1): "<",
        IntVector2(-1, 1): "v",
        IntVector2(0, 1): ">",
    },
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


def direction_to_key(direction: Direction) -> str:
    match direction:
        case Direction.UP:
            return "^"
        case Direction.LEFT:
            return "<"
        case Direction.RIGHT:
            return ">"
        case Direction.DOWN:
            return "v"


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


def find_keypad_sequence_part_one(target_code: str, proxies: int = 1) -> int:
    keypads = tuple([directional_keypad for _ in range(proxies)] + [numeric_keypad])
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


def find_keypad_sequence(target_code: str, proxies: int = 2) -> int:
    # still working on a Part Two implementation
    return find_keypad_sequence_part_one(target_code, proxies)
    steps = 0
    position = IntVector2(0, 0)
    for button in target_code:
        result = steps_to_press_button_detailed(
            button, numeric_keypad, position, directional_keypads_above=proxies + 1
        )
        steps += result[0]
        print(button, position, result[1])
        position = numeric_keypad.key_positions[button]
    return steps


def steps_to_press_button(
    target_button: str,
    keypad: Keypad,
    current_position: IntVector2,
    directional_keypads_above: int,
) -> int:
    return steps_to_press_button_detailed(
        target_button, keypad, current_position, directional_keypads_above
    )[0]


# @cache
def steps_to_press_button_detailed(
    target_button: str,
    keypad: Keypad,
    current_position: IntVector2,
    directional_keypads_above: int,
) -> tuple[int, str]:
    if directional_keypads_above == 0:
        # this is the direct keypad interface
        return (1, target_button)

    @dataclass(frozen=True)
    class Node:
        keypad_position: IntVector2
        upper_keypad_position: IntVector2

    start = Node(current_position, IntVector2(0, 0))
    frontier = PriorityQueue(start)
    cost_so_far: dict[Node, int] = {start: 0}
    came_from = dict[Node, tuple[Node, str]]()
    while (current := frontier.pop()) is not None:
        if keypad.keys[current.keypad_position] == target_button:
            buttons = list[str]()
            walkback = current
            while walkback != start:
                walkback, button = came_from[walkback]
                buttons.append(button)
            buttons.reverse()

            path = came_from[current][1] if current in came_from else ""

            steps_to_press_a = steps_to_press_button_detailed(
                "A",
                directional_keypad,
                current.upper_keypad_position,
                directional_keypads_above - 1,
            )

            return (
                cost_so_far[current] + steps_to_press_a[0],
                path + steps_to_press_a[1],
            )

        for direction in Direction:
            n = current.keypad_position + direction.to_vector()
            if not keypad.is_in_bounds(n):
                continue

            path = steps_to_press_button_detailed(
                direction_to_key(direction),
                directional_keypad,
                current.upper_keypad_position,
                directional_keypads_above - 1,
            )

            new_cost = cost_so_far[current] + path[0]
            new_node = Node(
                keypad_position=n,
                upper_keypad_position=directional_keypad.key_positions[
                    direction_to_key(direction)
                ],
            )
            if new_node not in cost_so_far or new_cost < cost_so_far[new_node]:
                cost_so_far[new_node] = new_cost
                frontier.add(new_node, new_cost)
                came_from[new_node] = (
                    current,
                    (came_from[current][1] if current in came_from else "")
                    + "".join(path[1]),
                )
    raise AssertionError("path not found")


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
