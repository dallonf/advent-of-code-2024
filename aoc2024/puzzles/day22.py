import aoc2024.common.input as aoc_input


def mix(value: int, secret: int) -> int:
    return value ^ secret


def prune(secret: int) -> int:
    return secret % 16_777_216


def next_secret(secret: int) -> int:
    result = secret * 64
    secret = mix(result, secret)
    secret = prune(secret)

    result = secret // 32
    secret = mix(result, secret)
    secret = prune(secret)

    result = secret * 2048
    secret = mix(result, secret)
    secret = prune(secret)

    return secret


def get_nth_secret(secret: int, n: int) -> int:
    for _ in range(n):
        secret = next_secret(secret)
    return secret


def part_one_answer(lines: list[str]) -> int:
    secrets = map(int, lines)
    return sum(get_nth_secret(s, 2000) for s in secrets)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day22input")
    print("Part One:", part_one_answer(puzzle_input))
