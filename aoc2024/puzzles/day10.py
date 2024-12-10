from collections import deque
from aoc2024.common.grid import BasicGrid, IntVector2
import aoc2024.common.input as aoc_input


class TopoMap:
    grid: BasicGrid[int | None]

    def __init__(self, grid: BasicGrid[int | None]):
        self.grid = grid

    @staticmethod
    def parse(lines: list[str]) -> "TopoMap":
        char_grid = BasicGrid.parse_char_grid(lines)
        grid = char_grid.map(lambda _, char: int(char) if char != "." else None)
        return TopoMap(grid)

    def score_trailhead(self, pos: IntVector2) -> int:
        assert self.grid[pos] == 0, "A trailhead must be a 0"
        explored = set[IntVector2]()
        found_trailtails = set[IntVector2]()
        explore_queue = deque[IntVector2]()
        explore_queue.append(pos)
        while len(explore_queue) > 0:
            exploring = explore_queue.popleft()
            explored.add(exploring)
            height = self.grid.get_if_in_bounds(exploring)
            if height is None:
                continue
            if height == 9:
                found_trailtails.add(exploring)
                continue

            next_height = height + 1
            neighbors = (exploring + d for d in IntVector2.cardinal_directions())
            eligible_neighbors = (
                n for n in neighbors if self.grid.get_if_in_bounds(n) == next_height
            )
            explore_queue.extend(eligible_neighbors)

        return len(found_trailtails)

    def score_all_trailheads(self) -> list[tuple[IntVector2, int]]:
        result = list[tuple[IntVector2, int]]()
        for coord, val in self.grid.all_items():
            if val == 0:
                score = self.score_trailhead(coord)
                if score > 0:
                    result.append((coord, score))
        return result


def part_one_answer(lines: list[str]) -> int:
    topomap = TopoMap.parse(lines)
    trailheads = topomap.score_all_trailheads()
    return sum(score for _, score in trailheads)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day10input")
    print("Part One:", part_one_answer(puzzle_input))
