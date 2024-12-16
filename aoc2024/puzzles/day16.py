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

    def get_path_length(self) -> int:
        start: PositionAndDirection = (self.start, Direction.RIGHT)
        frontier_by_priority: list[tuple[PositionAndDirection, int]] = [(start, 0)]
        cost_so_far = dict[PositionAndDirection, int]()
        cost_so_far[start] = 0

        while len(frontier_by_priority) > 0:
            current, _ = frontier_by_priority.pop()

            if current[0] == self.end:
                return cost_so_far[current]

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
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + next[0].manhattan_distance(self.end)
                    bisect.insort(
                        frontier_by_priority,
                        (next, priority),
                        # negative to ensure lowest estimated cost ("priority")
                        # is last, to be picked up by pop()
                        key=lambda x: -x[1],
                    )

        raise AssertionError("no path found")


def part_one_answer(lines: list[str]):
    maze = Maze.parse(lines)
    return maze.get_path_length()


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day16input")
    print("Part One:", part_one_answer(puzzle_input))
