import itertools
import aoc2024.common.input as aoc_input

type Report = list[int]


def parse_reports(lines: list[str]) -> list[Report]:
    return [parse_report(line) for line in lines]


def parse_report(line: str) -> Report:
    levels = line.split(" ")
    return [int(x) for x in levels]


def is_safe(report: Report) -> bool:
    direction = None
    for a, b in itertools.pairwise(report):
        if a > b:
            if direction == "increasing":
                return False
            direction = "decreasing"
        elif a < b:
            if direction == "decreasing":
                return False
            direction = "increasing"
        else:
            return False  # neither increasing nor decreasing

        diff = abs(a - b)
        if diff > 3:
            return False
    return True


def part_one_answer(lines: list[str]) -> int:
    reports = parse_reports(lines)
    return sum(1 if is_safe(r) else 0 for r in reports)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day02input")
    print("Part One:", part_one_answer(puzzle_input))
