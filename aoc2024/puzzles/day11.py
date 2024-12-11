import itertools
from typing import Callable, Iterable
import aoc2024.common.input as aoc_input


def parse(line: str):
    return [int(s) for s in line.split(" ")]


def blink(stones: list[int]) -> list[int]:
    def stone_reaction(label: int) -> list[int]:
        if label == 0:
            return [1]

        as_str = str(label)
        if len(as_str) % 2 == 0:
            midpoint = len(as_str) // 2
            return [int(as_str[0:midpoint]), int(as_str[midpoint:])]

        return [label * 2024]

    return list(flatmap(stone_reaction, stones))


def flatmap[T](func: Callable[[T], list[T]], *iterable: Iterable[T]):
    return itertools.chain.from_iterable(map(func, *iterable))


def multiblink(stones: list[int], times: int) -> list[int]:
    for _ in range(times):
        stones = blink(stones)
    return stones


def part_one_answer(puzzle_input: str) -> int:
    stones = parse(puzzle_input)
    stones = multiblink(stones, 25)
    return len(stones)


if __name__ == "__main__":
    puzzle_input = aoc_input.load("day11input")
    print("Part One:", part_one_answer(puzzle_input))
