from dataclasses import dataclass, replace
from enum import Enum, auto
import functools
from multiprocessing import Pool
from typing import Optional
from aoc2024.common.grid import BasicGrid, Direction, GridShape, IntVector2
import aoc2024.common.input as aoc_input


@dataclass(frozen=True)
class GuardMap:
    shape: GridShape
    obstacles: set[IntVector2]
    starting_position: IntVector2

    @staticmethod
    def parse(lines: list[str]):
        basic = BasicGrid.parse_char_grid(lines)
        obstacles = set[IntVector2]()
        starting_position = None
        for coord, entry in basic.all_items():
            if entry == "#":
                obstacles.add(coord)
            elif entry == "^":
                starting_position = coord
        assert starting_position != None
        return GuardMap(
            shape=basic.shape, obstacles=obstacles, starting_position=starting_position
        )

    def get_covered_positions(self):
        path = self.get_path()
        return set(x.position for x in path.states)

    def with_new_obstacle(self, new_obstacle: IntVector2) -> "GuardMap":
        obstacles = self.obstacles.copy()
        obstacles.add(new_obstacle)
        return replace(self, obstacles=obstacles)

    def get_path(self) -> "PathResult":
        past_states = list[GuardState]()
        past_states_set = set[GuardState]()
        guard_state = self.starting_state()

        while self.shape.is_in_bounds(guard_state.position):
            if guard_state in past_states_set:
                return PathResult(PathResultType.LOOPING, past_states)
            past_states.append(guard_state)
            past_states_set.add(guard_state)
            next_position = guard_state.next_position()
            if next_position in self.obstacles:
                guard_state = replace(
                    guard_state, direction=guard_state.direction.clockwise()
                )
            else:
                guard_state = replace(guard_state, position=next_position)

        return PathResult(PathResultType.EXITED, past_states)

    def starting_state(self):
        return GuardState(self.starting_position, Direction.UP)

    def get_possible_looping_obstructions(self):
        original_path = self.get_path()
        assert original_path.type == PathResultType.EXITED
        candidates = list(
            filter(
                lambda s: self.shape.is_in_bounds(s.next_position()),
                original_path.states,
            )
        )

        with Pool() as p:
            results = p.map(
                functools.partial(check_looping_obstruction, self),
                candidates,
            )
        # sync version
        # results = map(
        #     functools.partial(check_looping_obstruction, self),
        #     candidates,
        # )

        obstructions = [
            candidate.next_position()
            for (candidate, is_looping) in zip(candidates, results)
            if is_looping
        ]

        return set(obstructions)

    def part_one_result(self):
        return len(self.get_covered_positions())

    def part_two_result(self):
        return len(self.get_possible_looping_obstructions())


def check_looping_obstruction(
    guard_map: GuardMap, starting_state: "GuardState"
) -> bool:
    map_with_obstacle = guard_map.with_new_obstacle(starting_state.next_position())
    result = map_with_obstacle.get_path()
    return result.type == PathResultType.LOOPING


def debug_obstruction(guard_map: GuardMap, new_obstacle: IntVector2):
    map_with_obstacle = guard_map.with_new_obstacle(new_obstacle)
    path = map_with_obstacle.get_path()
    return path.debug(map_with_obstacle, new_obstacle=new_obstacle)


@dataclass(frozen=True, eq=True)
class GuardState:
    position: IntVector2
    direction: Direction

    def next_position(self):
        return self.position + self.direction.to_vector()


class PathResultType(Enum):
    EXITED = auto()
    LOOPING = auto()


@dataclass
class PathResult:
    type: "PathResultType"
    states: list["GuardState"]

    def debug(
        self,
        guard_map: GuardMap,
        /,
        new_obstacle: Optional[IntVector2] = None,
        include_starting_position: bool = True,
    ):
        shape = guard_map.shape
        char_map_data = list[str]("." for _ in range(shape.array_size()))
        for o in guard_map.obstacles:
            char_map_data[shape.array_index(o)] = "#"
        if new_obstacle is not None:
            char_map_data[shape.array_index(new_obstacle)] = "O"
        for state in self.states:
            current_char = char_map_data[shape.array_index(state.position)]
            new_char = None
            match (current_char, state.direction):
                case (".", Direction.UP) | (".", Direction.DOWN):
                    new_char = "|"
                case (".", Direction.LEFT) | (".", Direction.RIGHT):
                    new_char = "-"
                case (
                    ("-", Direction.UP)
                    | ("-", Direction.DOWN)
                    | ("|", Direction.RIGHT)
                    | ("|", Direction.LEFT)
                ):
                    new_char = "+"
                case ("-", Direction.LEFT) | ("-", Direction.RIGHT):
                    pass
                case ("|", Direction.UP) | ("|", Direction.DOWN):
                    pass
                case ("+", _):
                    pass
                case _:
                    raise AssertionError(
                        f"not sure how to handle {current_char}, {state.direction}"
                    )
            if new_char is not None:
                char_map_data[shape.array_index(state.position)] = new_char

        if include_starting_position:
            char_map_data[shape.array_index(guard_map.starting_position)] = "^"

        basic_grid = BasicGrid(char_map_data, shape.width)
        return basic_grid.format_char_grid()


if __name__ == "__main__":
    puzzle_input = GuardMap.parse(aoc_input.load_lines("day06input"))
    print("Part One", puzzle_input.part_one_result())
    print("Part Two (kinda slow)", puzzle_input.part_two_result())
