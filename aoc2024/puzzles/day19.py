from dataclasses import dataclass
from functools import cache
from typing import NewType
import aoc2024.common.input as aoc_input

Patterns = NewType("Patterns", tuple[str, ...])


@dataclass(frozen=True)
class PuzzleInput:
    patterns: Patterns
    designs: list[str]


def parse_patterns(line: str) -> Patterns:
    list = line.split(", ")
    list.sort()  # second alphabetically
    list.sort(
        reverse=True, key=lambda l: len(l)
    )  # first by length descending (i.e. longest first)
    return Patterns(tuple(list))


def parse(lines: list[str]) -> PuzzleInput:
    patterns = parse_patterns(lines[0])
    designs = lines[2:]
    return PuzzleInput(patterns, designs)


@cache
def is_design_possible(design: str, patterns: Patterns) -> bool:
    if len(design) == 0:
        return True

    for pattern in patterns:
        pattern_matches = design.startswith(pattern)
        if pattern_matches and is_design_possible(design[len(pattern) :], patterns):
            return True

    return False


@cache
def possible_arrangements(design: str, patterns: Patterns) -> int:
    result = 0
    for pattern in patterns:
        if design.startswith(pattern):
            is_terminal = len(design) - len(pattern) == 0
            if is_terminal:
                result += 1
            else:
                result += possible_arrangements(design[len(pattern) :], patterns)

    return result


def part_one_answer(lines: list[str]) -> int:
    puzzle_input = parse(lines)
    return sum(
        1 for d in puzzle_input.designs if is_design_possible(d, puzzle_input.patterns)
    )


def part_two_answer(lines: list[str]) -> int:
    puzzle_input = parse(lines)
    return sum(
        possible_arrangements(d, puzzle_input.patterns) for d in puzzle_input.designs
    )


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day19input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
