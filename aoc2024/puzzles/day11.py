from functools import cache
import itertools
from typing import Callable, Iterable, Sequence
import aoc2024.common.input as aoc_input


def parse(line: str):
    return tuple(int(s) for s in line.split(" "))


def stone_reaction(label: int) -> tuple[int, ...]:
    if label == 0:
        return (1,)

    as_str = str(label)
    if len(as_str) % 2 == 0:
        midpoint = len(as_str) // 2
        return (int(as_str[0:midpoint]), int(as_str[midpoint:]))

    return (label * 2024,)


def blink(stones: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(flatmap(stone_reaction, stones))


def flatmap[T](func: Callable[[T], Sequence[T]], *iterable: Iterable[T]):
    return itertools.chain.from_iterable(map(func, *iterable))


def count_after_blinks(stones: tuple[int, ...], times: int) -> int:
    return sum(count_single_stone_after_blinks(s, times) for s in stones)


@cache
def count_single_stone_after_blinks(label: int, times: int) -> int:
    if times == 0:
        return 1
    split = stone_reaction(label)
    return sum(count_single_stone_after_blinks(s, times - 1) for s in split)


def part_one_answer(puzzle_input: str) -> int:
    stones = parse(puzzle_input)
    return count_after_blinks(stones, 25)


def part_two_answer(puzzle_input: str) -> int:
    stones = parse(puzzle_input)
    return count_after_blinks(stones, 75)


if __name__ == "__main__":
    puzzle_input = aoc_input.load("day11input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
