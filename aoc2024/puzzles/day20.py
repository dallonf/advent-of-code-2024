import bisect
from dataclasses import dataclass, replace
from enum import Enum, auto
from functools import cache
from typing import Optional, cast
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

    @cache
    def get_legit_path(self) -> list[IntVector2]:
        frontier_by_priority: list[tuple[IntVector2, int]] = [(self.start, 0)]
        cost_so_far = dict[IntVector2, int]()
        cost_so_far[self.start] = 0
        came_from = dict[IntVector2, IntVector2]()

        while len(frontier_by_priority) > 0:
            current, _ = frontier_by_priority.pop()

            if current == self.end:
                path = list[IntVector2]()
                walkback = self.end
                while walkback != self.start:
                    path.append(walkback)
                    walkback = came_from[walkback]
                path.reverse()
                return path

            for next in current.cardinal_neighbors():
                if not self.walls.shape.is_in_bounds(next) or self.walls[next]:
                    continue
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + next.manhattan_distance(self.end)
                    bisect.insort(
                        frontier_by_priority, (next, priority), key=lambda it: -it[1]
                    )
                    came_from[next] = current

        raise AssertionError("No path found")

    def try_cheat(
        self, start: IntVector2, end: IntVector2, max_length: int
    ) -> Cheat | None:
        frontier_by_priority = list[tuple[IntVector2, int]]([(end, 0)])
        cost_so_far = dict[IntVector2, int]()
        cost_so_far[end] = 0

        while len(frontier_by_priority) > 0:
            current, _ = frontier_by_priority.pop()
            if cost_so_far[current] > max_length:
                return None

            if current == self.end:
                return Cheat(start, end, cost_so_far[current])

            for next in current.cardinal_neighbors():
                if not self.walls.shape.is_in_bounds(next) or self.walls[next]:
                    continue
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + next.manhattan_distance(self.end)
                    bisect.insort(
                        frontier_by_priority, (next, priority), key=lambda it: -it[1]
                    )

        return None

    def find_cheats(self, minimum_savings: int = 1) -> CheatsBySavedTime:
        result = dict[int, int]()
        legit_path = self.get_legit_path()

        for length_so_far, position in enumerate(legit_path[:-1]):
            length_so_far += 1  # path does not include the start node
            for n in position.cardinal_neighbors():
                if self.walls.shape.is_in_bounds(n):
                    expected_length = len(legit_path) - length_so_far
                    if expected_length < minimum_savings:
                        continue
                    cheat = self.try_cheat(
                        start=position,
                        end=n,
                        max_length=expected_length - minimum_savings,
                    )
                    if cheat is not None:
                        time_save = expected_length - (
                            cheat.path_length + length_so_far
                        )
                        if time_save < 0:
                            # try_cheat's max_length should be catching this
                            continue
                        result.setdefault(time_save, 0)
                        result[time_save] += 1

        return result


def part_one_answer(lines: list[str]):
    maze = Maze.parse(lines)
    cheats = maze.find_cheats()
    return sum(v for v in cheats.values())


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day20input")
    print("Part One:", part_one_answer(puzzle_input))
