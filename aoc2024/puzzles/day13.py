from dataclasses import dataclass, replace
from functools import cached_property
import itertools
import re
from typing import Sequence
from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input


button_regex = re.compile(r"Button (?:A|B): X\+([0-9]+), Y\+([0-9]+)")
prize_regex = re.compile(r"Prize: X=([0-9]+), Y=([0-9]+)")


@dataclass(frozen=True)
class OptimalPresses:
    a: int
    b: int

    @cached_property
    def cost(self):
        return self.a * 3 + self.b


@dataclass(frozen=True)
class Machine:
    button_a: IntVector2
    button_b: IntVector2
    prize: IntVector2

    @staticmethod
    def parse(lines: Sequence[str]) -> "Machine":
        assert len(lines) == 3, "a machine requires a 3-line input"
        button_a_match = button_regex.match(lines[0])
        button_b_match = button_regex.match(lines[1])
        prize_match = prize_regex.match(lines[2])
        assert button_a_match and button_b_match and prize_match
        button_a = IntVector2(
            int(button_a_match.group(1)), int(button_a_match.group(2))
        )
        button_b = IntVector2(
            int(button_b_match.group(1)), int(button_b_match.group(2))
        )
        prize = IntVector2(int(prize_match.group(1)), int(prize_match.group(2)))
        return Machine(button_a=button_a, button_b=button_b, prize=prize)

    def get_optimal_presses(self) -> OptimalPresses | None:
        # don't ask me to explain how this works, I used ChatGPT lol
        det = self.button_a.x * self.button_b.y - self.button_a.y * self.button_b.x
        if det == 0:
            return None
        a_wip = self.button_b.y * self.prize.x - self.button_b.x * self.prize.y
        b_wip = -self.button_a.y * self.prize.x + self.button_a.x * self.prize.y

        if a_wip % det != 0 or b_wip % det != 0:
            # the answer won't be an integer
            return None

        return OptimalPresses(a_wip // det, b_wip // det)

    def corrected(self) -> "Machine":
        offset = 10_000_000_000_000
        return replace(self, prize=self.prize + IntVector2(offset, offset))


def parse_all(lines: list[str]) -> list[Machine]:
    results = list[Machine]()
    for batch in itertools.batched(lines, 4, strict=False):
        results.append(Machine.parse(batch[:3]))
    return results


def part_one_answer(lines: list[str]) -> int:
    machines = parse_all(lines)
    results = (m.get_optimal_presses() for m in machines)
    costs = (o.cost for o in results if o is not None)
    return sum(costs)


def part_two_answer(lines: list[str]) -> int:
    machines = parse_all(lines)
    results = (m.corrected().get_optimal_presses() for m in machines)
    costs = (o.cost for o in results if o is not None)
    return sum(costs)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day13input")
    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
