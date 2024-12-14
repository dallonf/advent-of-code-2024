from dataclasses import dataclass, replace
import re
from aoc2024.common.grid import GridShape, IntVector2
import aoc2024.common.input as aoc_input


def sample_shape() -> GridShape:
    return GridShape(11, 7)


def real_shape() -> GridShape:
    return GridShape(101, 103)


@dataclass
class Robot:
    position: IntVector2
    velocity: IntVector2

    @staticmethod
    def parse(line: str) -> "Robot":
        match = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
        assert match is not None
        int_groups = [int(m) for m in match.groups()]
        return Robot(
            IntVector2(int_groups[0], int_groups[1]),
            IntVector2(int_groups[2], int_groups[3]),
        )

    @staticmethod
    def parse_all(lines: list[str]) -> "list[Robot]":
        return [Robot.parse(line) for line in lines]

    def move(self, shape: GridShape, times: int = 1) -> None:
        self.position += self.velocity * times
        if self.position.y < 0:
            self.position = replace(
                self.position, y=shape.height + (self.position.y % shape.height)
            )
        if self.position.x < 0:
            self.position = replace(
                self.position, x=shape.width + (self.position.x % shape.width)
            )
        if self.position.x >= shape.width:
            self.position = replace(self.position, x=self.position.x % shape.width)
        if self.position.y >= shape.height:
            self.position = replace(self.position, y=self.position.y % shape.height)


def count_by_quadrant(
    robots: list[Robot], shape: GridShape
) -> tuple[int, int, int, int]:
    "top-left, top-right, bottom-left, bottom-right"
    assert (
        shape.width % 2 == 1 and shape.height % 2 == 1
    ), "shape width/hieght must be odd numbers"

    mid_x = shape.width // 2
    mid_y = shape.height // 2

    top_left = sum(1 for r in robots if r.position.x < mid_x and r.position.y < mid_y)
    top_right = sum(1 for r in robots if r.position.x > mid_x and r.position.y < mid_y)
    bottom_left = sum(
        1 for r in robots if r.position.x < mid_x and r.position.y > mid_y
    )
    bottom_right = sum(
        1 for r in robots if r.position.x > mid_x and r.position.y > mid_y
    )

    return (top_left, top_right, bottom_left, bottom_right)


def debug_robot_counts(robots: list[Robot], shape: GridShape) -> str:
    robot_position_counts = dict[IntVector2, int]()
    for r in robots:
        if r.position in robot_position_counts:
            robot_position_counts[r.position] += 1
        else:
            robot_position_counts[r.position] = 1
    return shape.format(
        lambda pos: (
            str(robot_position_counts[pos]) if pos in robot_position_counts else "."
        )
    )


def part_one_answer(lines: list[str], shape: GridShape = real_shape()) -> int:
    robots = Robot.parse_all(lines)
    for r in robots:
        r.move(shape, 100)
    quadrants = count_by_quadrant(robots, shape)
    result = 1
    for q in quadrants:
        result *= q
    return result


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day14input")
    print("Part One:", part_one_answer(puzzle_input))
