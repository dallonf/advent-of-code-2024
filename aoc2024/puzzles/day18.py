import bisect
from functools import cached_property
from typing import Optional, Sequence
from aoc2024.common.grid import GridShape, IntVector2
import aoc2024.common.input as aoc_input


def sample_shape() -> GridShape:
    return GridShape(7, 7)


def real_shape() -> GridShape:
    return GridShape(71, 71)


class Region:
    shape: GridShape
    obstacles: set[IntVector2]

    def __init__(self, shape: GridShape):
        self.shape = shape
        self.obstacles = set()

    @cached_property
    def exit(self):
        return IntVector2(self.shape.width - 1, self.shape.height - 1)

    def add_obstacles(self, obstacles: Sequence[IntVector2]):
        self.obstacles.update(obstacles)

    def add_obstacle(self, obstacle: IntVector2):
        self.obstacles.add(obstacle)

    def find_path(self) -> Optional[tuple[int, list[IntVector2]]]:
        start = IntVector2(0, 0)

        frontier_by_priority: list[tuple[IntVector2, int]] = [(start, 0)]
        cost_so_far = dict[IntVector2, int]()
        cost_so_far[start] = 0
        came_from = dict[IntVector2, IntVector2]()

        while len(frontier_by_priority) > 0:
            current, _ = frontier_by_priority.pop()

            if current == self.exit:
                path = list[IntVector2]()
                walkback = self.exit
                while walkback != start:
                    path.append(walkback)
                    walkback = came_from[walkback]
                return (cost_so_far[current], path)

            for next in current.cardinal_neighbors():
                if not self.shape.is_in_bounds(next) or next in self.obstacles:
                    continue
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + next.manhattan_distance(self.exit)
                    bisect.insort(
                        frontier_by_priority, (next, priority), key=lambda it: -it[1]
                    )
                    came_from[next] = current

        return None

    def debug(self):
        return self.shape.format(lambda coord: "#" if coord in self.obstacles else ".")


def parse_obstacles(lines: list[str]) -> list[IntVector2]:
    result = list[IntVector2]()
    for l in lines:
        x, y = l.split(",")
        result.append(IntVector2(int(x), int(y)))
    return result


def part_one_answer(
    lines: list[str], shape: GridShape = real_shape(), falling_ticks: int = 1024
) -> int:
    obstacles = parse_obstacles(lines)
    region = Region(shape)
    region.add_obstacles(obstacles[:falling_ticks])
    path = region.find_path()
    if path is None:
        raise AssertionError("no path found")
    return path[0]


def part_two_answer(lines: list[str], shape: GridShape = real_shape()) -> str:
    obstacles = parse_obstacles(lines)
    region = Region(shape)
    path = region.find_path()
    if path is None:
        raise AssertionError("no path found initially")
    steps_along_path = set(path[1])
    for o in obstacles:
        region.add_obstacle(o)
        # recalculate path if the current path gets blocked
        if o in steps_along_path:
            path = region.find_path()
            if path is None:
                return f"{o.x},{o.y}"
            steps_along_path = set(path[1])

    raise AssertionError("Operation completed successfully (path was never blocked)")


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day18input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
