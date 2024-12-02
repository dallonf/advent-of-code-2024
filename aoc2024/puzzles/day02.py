import aoc2024.common.input as aoc_input


def parse_reports(lines: list[str]) -> list[list[int]]:
    return [parse_report(line) for line in lines]


def parse_report(line: str) -> list[int]:
    levels = line.split(" ")
    return [int(x) for x in levels]


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day02input")
