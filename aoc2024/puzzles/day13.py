from dataclasses import dataclass
import itertools
import re
from typing import Sequence
from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input


button_regex = re.compile(r"Button (?:A|B): X\+([0-9]+), Y\+([0-9]+)")
prize_regex = re.compile(r"Prize: X=([0-9]+), Y=([0-9]+)")


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


def parse_all(lines: list[str]) -> list[Machine]:
    results = list[Machine]()
    for batch in itertools.batched(lines, 4, strict=False):
        results.append(Machine.parse(batch[:3]))
    return results


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day13input")
