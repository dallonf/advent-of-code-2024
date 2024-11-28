import aoc2024.common.input as aoc_input


def uppercase(lines: list[str]) -> list[str]:
    return [line.upper() for line in lines]


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day00sample")

    print("result:", uppercase(puzzle_input))
