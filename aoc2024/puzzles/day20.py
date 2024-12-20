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
    cheat_start: Optional[IntVector2] = None
    cheat_end: Optional[IntVector2] = None


type CheatsBySavedTime = dict[int, int]


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

    def find_cheats(self, minimum_savings: int = 1) -> CheatsBySavedTime:
        result = dict[int, int]()
        legit_path = self.get_legit_path()

        frontier_by_priority = list[tuple[PathfindingNode, int]]()
        cost_so_far = dict[PathfindingNode, int]()
        discovered_cheats = set[tuple[IntVector2, IntVector2]]()

        for cost, position in enumerate(legit_path):
            cost += 1  # path does not include the start node (cost 0)
            priority = cost + position.manhattan_distance(self.end)
            node = PathfindingNode(position)
            frontier_by_priority.append((node, priority))
            cost_so_far[node] = cost
        frontier_by_priority.sort(key=lambda it: -it[1])

        while len(frontier_by_priority) > 0:
            current, cost = frontier_by_priority.pop()
            if cost > len(legit_path) - minimum_savings:
                return result

            if current.position == self.end:
                assert current.cheat_start is not None and current.cheat_end is not None
                cheat = (current.cheat_start, current.cheat_end)
                if cheat in discovered_cheats:
                    continue
                time_save = len(legit_path) - cost_so_far[current]
                result.setdefault(time_save, 0)
                result[time_save] += 1
                discovered_cheats.add(cheat)

            match current.cheat_state:
                case CheatState.Allowed:
                    # since all of the initial path is in the frontier,
                    # we should definitely start cheating right away from each node
                    neighbors = [
                        PathfindingNode(
                            n, CheatState.Cheating, cheat_start=current.position
                        )
                        for n in current.position.cardinal_neighbors()
                        if self.walls.get_if_in_bounds(n)
                    ]
                case CheatState.Cheating:
                    # Need to get back on course
                    neighbors = [
                        replace(
                            current,
                            position=n,
                            cheat_state=CheatState.Done,
                            cheat_end=current.position,
                        )
                        for n in current.position.cardinal_neighbors()
                        if self.walls.shape.is_in_bounds(n) and not self.walls[n]
                    ]
                case CheatState.Done:
                    # back to normal physics
                    neighbors = [
                        replace(current, position=n, cheat_state=CheatState.Done)
                        for n in current.position.cardinal_neighbors()
                        if self.walls.shape.is_in_bounds(n) and not self.walls[n]
                    ]

            for next in neighbors:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + next.position.manhattan_distance(self.end)
                    bisect.insort(
                        frontier_by_priority, (next, priority), key=lambda it: -it[1]
                    )

        return result


def part_one_answer(lines: list[str]):
    maze = Maze.parse(lines)
    cheats = maze.find_cheats()
    return sum(v for v in cheats.values())


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day20input")
    print("Part One:", part_one_answer(puzzle_input))
