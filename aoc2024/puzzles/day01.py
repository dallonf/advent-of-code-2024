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


def get_distances(lists: ListPair) -> list[int]:
    sorted_lists = (lists[0].copy(), lists[1].copy())
    sorted_lists[0].sort()
    sorted_lists[1].sort()

    distances: list[int] = []
    for a, b in zip(*sorted_lists):
        distance = abs(a - b)
        distances.append(distance)

    return distances


def part_one_solution(input_data: str) -> int:
    lists = parse_lists(input_data)
    distances = get_distances(lists)
    return sum(distances)


if __name__ == "__main__":
    puzzle_input = aoc_input.load("day01input")
    print(part_one_solution(puzzle_input))
