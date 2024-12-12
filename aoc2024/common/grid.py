from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
from typing import Callable, Iterator, Optional, Self


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def to_vector(self):
        match self:
            case Direction.UP:
                return IntVector2(0, -1)
            case Direction.DOWN:
                return IntVector2(0, 1)
            case Direction.LEFT:
                return IntVector2(-1, 0)
            case Direction.RIGHT:
                return IntVector2(1, 0)

    def clockwise(self):
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

    def counter_clockwise(self):
        match self:
            case Direction.UP:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.UP


@dataclass(frozen=True)
class IntVector2:
    x: int
    y: int

    def __add__(self, other: Self):
        return IntVector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self):
        return IntVector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return IntVector2(self.x * other, self.y * other)

    @staticmethod
    def cardinal_directions() -> Iterator["IntVector2"]:
        yield IntVector2(0, -1)
        yield IntVector2(1, 0)
        yield IntVector2(0, 1)
        yield IntVector2(-1, 0)

    def cardinal_neighbors(self) -> Iterator["IntVector2"]:
        return (self + d for d in IntVector2.cardinal_directions())

    @staticmethod
    def diagonal_directions() -> Iterator["IntVector2"]:
        yield IntVector2(1, -1)
        yield IntVector2(1, 1)
        yield IntVector2(-1, 1)
        yield IntVector2(-1, -1)

    @staticmethod
    def eight_directions() -> Iterator["IntVector2"]:
        yield from IntVector2.cardinal_directions()
        yield from IntVector2.diagonal_directions()

    type IntoIntVector = IntVector2 | tuple[int, int]

    @staticmethod
    def normalize_input(x: IntoIntVector) -> "IntVector2":
        if isinstance(x, IntVector2):
            return x
        else:
            return IntVector2(x[0], x[1])


@dataclass
class GridShape:
    width: int
    height: int

    def array_index(self, coord: IntVector2) -> int:
        "Does not support a negative coord"
        return coord.y * self.width + coord.x

    def array_size(self) -> int:
        return self.width * self.height

    def coordinate_for_index(self, index: int) -> IntVector2:
        return IntVector2((index % self.width), index // self.width)

    def all_coords(self) -> Iterator[IntVector2]:
        for y in range(self.height):
            for x in range(self.width):
                yield IntVector2(x, y)

    def is_in_bounds(self, coord: IntVector2) -> bool:
        return (
            coord.x >= 0
            and coord.y >= 0
            and coord.x < self.width
            and coord.y < self.height
        )


class BasicGrid[T]:
    _width: int
    items: list[T]

    def __init__(self, items: list[T], width: int):
        self.items = items
        self._width = width

    @property
    def width(self):
        return self._width

    @cached_property
    def shape(self) -> GridShape:
        return GridShape(self.width, len(self.items) // self.width)

    def __getitem__(self, key: IntVector2.IntoIntVector) -> T:
        return self.items[self.shape.array_index(IntVector2.normalize_input(key))]

    def __setitem__(self, key: IntVector2.IntoIntVector, value: T):
        self.items[self.shape.array_index(IntVector2.normalize_input(key))] = value

    def get_if_in_bounds(self, key: IntVector2.IntoIntVector) -> Optional[T]:
        key = IntVector2.normalize_input(key)
        if self.shape.is_in_bounds(key):
            return self[key]
        else:
            return None

    @staticmethod
    def parse_char_grid(lines: list[str]) -> "BasicGrid[str]":
        expected_width = len(lines[0])
        items: list[str] = []
        for i, line in enumerate(lines):
            assert len(line) == expected_width, f"mismatched width for line {i}"
            items += list(line)
        return BasicGrid(items, expected_width)

    def map[
        Output
    ](self, func: Callable[[IntVector2, T], Output]) -> "BasicGrid[Output]":
        new_list = list(
            map(
                lambda x: func(self.shape.coordinate_for_index(x[0]), x[1]),
                enumerate(self.items),
            )
        )
        return BasicGrid(new_list, self.width)

    def format_char_grid(self: "BasicGrid[str]") -> str:
        lines: list[str] = []
        for y in range(self.shape.height):
            start = self.shape.array_index(IntVector2(0, y))
            end = self.shape.array_index(IntVector2(0, y + 1))
            lines.append("".join(self.items[start:end]))
        return "\n".join(lines)

    def copy(self) -> "BasicGrid[T]":
        return BasicGrid(self.items.copy(), self.width)

    def all_items(self) -> Iterator[tuple[IntVector2, T]]:
        for coord in self.shape.all_coords():
            yield (coord, self[coord])
