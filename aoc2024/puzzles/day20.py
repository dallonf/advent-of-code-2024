import bisect
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from functools import cache
import sys
from typing import Iterator, Optional, Sequence, cast
from aoc2024.common.grid import BasicGrid, IntVector2
import aoc2024.common.input as aoc_input


class CheatState(Enum):
    Allowed = auto()
    Cheating = auto()
    Done = auto()


@dataclass(frozen=True)
class PathfindingNode:
    position: IntVector2
    cheat_state: CheatState = CheatState.Allowed


type CheatsBySavedTime = dict[int, int]


@dataclass(frozen=True)
class Cheat:
    start: IntVector2
    end: IntVector2
    path_length: int


@dataclass(frozen=True)
class Maze:
    walls: BasicGrid[bool]
    start: IntVector2
    end: IntVector2

    @staticmethod
    def parse(lines: list[str]):
        char_grid = BasicGrid.parse_char_grid(lines)
        start = cast(Optional[IntVector2], None)
        end = cast(Optional[IntVector2], None)

        def each_char(coord: IntVector2, char: str) -> bool:
            nonlocal start, end
            match char:
                case ".":
                    return False
                case "#":
                    return True
                case "S":
                    start = coord
                    return False
                case "E":
                    end = coord
                    return False
                case _:
                    raise AssertionError(f"unexpected char in grid: {char}")

        walls = char_grid.map(each_char)
        assert start is not None and end is not None
        return Maze(walls, start, end)

    def is_passable(self, coord: IntVector2):
        return self.walls.shape.is_in_bounds(coord) and not self.walls[coord]

    @cache
    def get_flow_map(self) -> BasicGrid[int | None]:
        flow_map = BasicGrid[int | None].filled(self.walls.shape, None)
        queue = deque[tuple[IntVector2, int]]()
        queue.append((self.end, 0))
        while len(queue) > 0:
            current, distance = queue.popleft()
            if self.is_passable(current):
                prev_distance = flow_map[current]
                if prev_distance is None or distance < prev_distance:
                    flow_map[current] = distance
                    queue.extend(
                        ((n, distance + 1) for n in current.cardinal_neighbors())
                    )

        return flow_map

    @cache
    def get_legit_path(self) -> list[IntVector2]:
        flow_map = self.get_flow_map()
        path = [self.start]
        while (current := path[-1]) != self.end:
            neighbors = [
                (n, flow_map.get_if_in_bounds(n)) for n in current.cardinal_neighbors()
            ]
            best_neighbor = min(
                neighbors, key=lambda it: it[1] if it[1] is not None else sys.maxsize
            )
            assert best_neighbor[1] is not None, "Couldn't find path"
            path.append(best_neighbor[0])

        # don't include the start node
        path.pop(0)

        return path

    def find_cheats(
        self, minimum_savings: int = 1, cheat_length: int = 2
    ) -> CheatsBySavedTime:
        legit_length = len(self.get_legit_path())
        max_length = legit_length - minimum_savings

        discovered = dict[tuple[IntVector2, IntVector2], int]()
        flow_map = self.get_flow_map()

        frontier_by_priority: list[tuple[IntVector2, int]] = [(self.start, 0)]
        cost_so_far = dict[IntVector2, int]()
        cost_so_far[self.start] = 0

        def add_to_frontier(node: IntVector2, cost: int):
            if node not in cost_so_far or cost < cost_so_far[node]:
                cost_so_far[node] = cost
                priority = cost + n.manhattan_distance(self.end)
                bisect.insort(
                    frontier_by_priority, (node, priority), key=lambda it: -it[1]
                )

        def result():
            grouped = dict[int, int]()
            for v in discovered.values():
                saved_time = legit_length - v
                grouped.setdefault(saved_time, 0)
                grouped[saved_time] += 1
            return grouped

        while len(frontier_by_priority) > 0:
            current, _ = frontier_by_priority.pop()

            if current == self.end or cost_so_far[current] > max_length:
                # no further cheats are optimal
                return result()

            for n in current.cardinal_neighbors():
                new_cost = cost_so_far[current] + 1
                if self.is_passable(n):
                    add_to_frontier(n, new_cost)

            cheat_start = current
            for cheat_end in get_surrounding(cheat_start, cheat_length):
                remaining_cost = flow_map.get_if_in_bounds(cheat_end)
                if remaining_cost is not None and cheat_end not in cost_so_far:
                    total_length = (
                        cost_so_far[current]
                        + cheat_end.manhattan_distance(cheat_start)
                        + remaining_cost
                    )
                    if total_length > max_length:
                        continue
                    already_discovered = discovered.get((cheat_start, cheat_end))
                    if already_discovered is None or total_length < already_discovered:
                        discovered[(cheat_start, cheat_end)] = total_length

        return result()


def get_surrounding(coord: IntVector2, steps: int) -> set[IntVector2]:
    distances = dict[IntVector2, int]()
    queue = deque[tuple[IntVector2, int]]([(coord, 0)])

    while len(queue) > 0:
        current, current_distance = queue.popleft()
        if current_distance > steps or current in distances:
            continue

        distances[current] = current_distance
        queue.extend((n, current_distance + 1) for n in current.cardinal_neighbors())

    distances.pop(coord)  # the start is not surrounding itself
    return set((k for k, v in distances.items() if v <= steps))


def part_one_answer(lines: list[str]):
    maze = Maze.parse(lines)
    cheats = maze.find_cheats(minimum_savings=100)
    return sum(v for v in cheats.values())


def part_two_answer(lines: list[str]):
    maze = Maze.parse(lines)
    cheats = maze.find_cheats(minimum_savings=100, cheat_length=20)
    return sum(v for v in cheats.values())


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day20input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
