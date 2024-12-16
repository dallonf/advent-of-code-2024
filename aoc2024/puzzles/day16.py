from collections import deque
from dataclasses import dataclass
from typing import Optional, cast
from aoc2024.common.grid import BasicGrid, Direction, IntVector2
import bisect
import aoc2024.common.input as aoc_input

type PositionAndDirection = tuple[IntVector2, Direction]


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

    @dataclass(frozen=True)
    class PathResults:
        score: int
        visited_positions: set[IntVector2]

    def explore_path(self) -> "PathResults":
        start: PositionAndDirection = (self.start, Direction.RIGHT)
        frontier_by_priority: list[tuple[PositionAndDirection, int]] = [(start, 0)]
        cost_so_far = dict[PositionAndDirection, int]()
        cost_so_far[start] = 0
        came_from = dict[PositionAndDirection, set[PositionAndDirection]]()
        best_score = None

        while len(frontier_by_priority) > 0:
            current, _ = frontier_by_priority.pop()

            if current[0] == self.end:
                if best_score is None:
                    best_score = cost_so_far[current]
                if best_score > cost_so_far[current]:
                    # we're now finding inferior paths
                    break

            clockwise = current[1].clockwise()
            counter_clockwise = current[1].counter_clockwise()

            neighbors_and_costs: list[tuple[PositionAndDirection, int]] = [
                ((current[0] + current[1].to_vector(), current[1]), 1),
                ((current[0] + clockwise.to_vector(), clockwise), 1001),
                ((current[0] + counter_clockwise.to_vector(), counter_clockwise), 1001),
            ]
            neighbors_and_costs = [
                n for n in neighbors_and_costs if not self.walls[n[0][0]]
            ]
            for next, next_cost in neighbors_and_costs:
                new_cost = cost_so_far[current] + next_cost
                if next not in cost_so_far or new_cost <= cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + next[0].manhattan_distance(self.end)
                    bisect.insort(
                        frontier_by_priority,
                        (next, priority),
                        # negative to ensure lowest estimated cost ("priority")
                        # is last, to be picked up by pop()
                        key=lambda x: -x[1],
                    )
                    existing_came_from = came_from.setdefault(next, set())
                    if next in cost_so_far and new_cost < cost_so_far[next]:
                        existing_came_from.clear()
                    existing_came_from.add(current)

        if best_score is None:
            raise AssertionError("no path found")

        visited_positions = set[IntVector2]()
        backtrack_queue = deque[PositionAndDirection]((self.end, d) for d in Direction)
        while len(backtrack_queue) > 0:
            current = backtrack_queue.popleft()
            if current in cost_so_far and cost_so_far[current] > best_score:
                continue
            visited_positions.add(current[0])
            prev_nodes = came_from.get(current) or set()
            backtrack_queue.extend(prev_nodes)
        return Maze.PathResults(best_score, visited_positions)

    def get_path_score(self):
        results = self.explore_path()
        return results.score

    def get_best_seats(self):
        results = self.explore_path()
        return results.visited_positions


def part_one_answer(lines: list[str]):
    maze = Maze.parse(lines)
    return maze.get_path_score()


def part_two_answer(lines: list[str]):
    maze = Maze.parse(lines)
    return len(maze.get_best_seats())


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day16input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
