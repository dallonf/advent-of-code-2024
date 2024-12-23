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


def get_sequences(
    initial_secret: int, iterations: int = 2000
) -> dict[tuple[int, int, int, int], int]:
    result = dict[tuple[int, int, int, int], int]()
    prices = list[int]()
    changes = list[int]()
    secret = initial_secret
    last_price = initial_secret % 10
    for _ in range(iterations):
        new_secret = next_secret(secret)
        new_price = new_secret % 10
        prices.append(new_price)
        changes.append(new_price - last_price)
        last_price = new_price
        secret = new_secret
    assert len(prices) == len(changes)
    for i in range(3, len(changes)):
        sequence = (changes[i - 3], changes[i - 2], changes[i - 1], changes[i])
        price = prices[i]
        if sequence not in result:
            result[sequence] = price
    return result


def optimize_purchases(
    initial_secrets: list[int],
    iterations: int = 2000,
) -> tuple[tuple[int, int, int, int], int]:
    candidates = dict[tuple[int, int, int, int], int]()
    for secret in initial_secrets:
        sequences = get_sequences(secret, iterations)
        for sequence, price in sequences.items():
            candidates.setdefault(sequence, 0)
            candidates[sequence] += price
    return max(candidates.items(), key=lambda it: it[1])


def part_two_answer(lines: list[str]) -> int:
    secrets = map(int, lines)
    result = optimize_purchases(list(secrets))
    return result[1]


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day22input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
