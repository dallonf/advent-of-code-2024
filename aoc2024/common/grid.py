from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
from typing import Iterator, Optional, Self


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def to_vector(self):
        match self:
            case Direction.UP:
                return IntVector(0, -1)
            case Direction.DOWN:
                return IntVector(0, 1)
            case Direction.LEFT:
                return IntVector(-1, 0)
            case Direction.RIGHT:
                return IntVector(1, 0)


@dataclass(frozen=True)
class IntVector:
    x: int
    y: int

    def __add__(self, other: Self):
        return IntVector(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return IntVector(self.x * other, self.y * other)

    @staticmethod
    def cardinal_directions() -> Iterator["IntVector"]:
        yield IntVector(0, -1)
        yield IntVector(1, 0)
        yield IntVector(0, 1)
        yield IntVector(-1, 0)

    @staticmethod
    def diagonal_directions() -> Iterator["IntVector"]:
        yield IntVector(1, -1)
        yield IntVector(1, 1)
        yield IntVector(-1, 1)
        yield IntVector(-1, -1)

    @staticmethod
    def eight_directions() -> Iterator["IntVector"]:
        yield from IntVector.cardinal_directions()
        yield from IntVector.diagonal_directions()

    type IntoIntVector = IntVector | tuple[int, int]

    @staticmethod
    def normalize_input(x: IntoIntVector) -> "IntVector":
        if isinstance(x, IntVector):
            return x
        else:
            return IntVector(x[0], x[1])


@dataclass
class GridShape:
    width: int
    height: int

    def array_index(self, coord: IntVector) -> int:
        "Does not support a negative coord"
        return coord.y * self.width + coord.x

    def coordinate_for_index(self, index: int) -> IntVector:
        return IntVector((index % self.width), index // self.width)

    def all_coords(self) -> Iterator[IntVector]:
        for y in range(self.height):
            for x in range(self.width):
                yield IntVector(x, y)

    def is_in_bounds(self, coord: IntVector) -> bool:
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

    def __getitem__(self, key: IntVector.IntoIntVector) -> T:
        return self.items[self.shape.array_index(IntVector.normalize_input(key))]

    def __setitem__(self, key: IntVector.IntoIntVector, value: T):
        self.items[self.shape.array_index(IntVector.normalize_input(key))] = value

    def get_if_in_bounds(self, key: IntVector.IntoIntVector) -> Optional[T]:
        key = IntVector.normalize_input(key)
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

    def format_char_grid(self: "BasicGrid[str]") -> str:
        lines: list[str] = []
        for y in range(self.shape.height):
            start = self.shape.array_index(IntVector(0, y))
            end = self.shape.array_index(IntVector(0, y + 1))
            lines.append("".join(self.items[start:end]))
        return "\n".join(lines)

    def copy(self) -> "BasicGrid[T]":
        return BasicGrid(self.items.copy(), self.width)
