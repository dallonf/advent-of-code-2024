import aoc2024.common.input as aoc_input


type ListPair = tuple[list[int], list[int]]


def parse_lists(input_data: str) -> ListPair:
    list1: list[int] = []
    list2: list[int] = []
    input_lines = aoc_input.lines(input_data)

    for line in input_lines:
        [entry1, entry2] = line.split("   ")
        list1.append(int(entry1))
        list2.append(int(entry2))

    return (list1, list2)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day01input")
