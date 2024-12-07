from dataclasses import dataclass
import itertools
import math
from multiprocessing import Pool
import time
from typing import Iterable, Literal
import aoc2024.common.input as aoc_input

SIMPLE_OPERATORS = ("+", "*")
COMPLEX_OPERATORS = (
    "+",
    "*",
    "||",
)


@dataclass
class Equation:
    test_value: int
    values: list[int]

    @staticmethod
    def parse(line: str) -> "Equation":
        test_value, values = line.split(": ")
        test_value = int(test_value)
        values = list(map(int, values.split(" ")))
        return Equation(test_value, values)

    def can_be_valid(
        self,
        /,
        operators: Iterable[
            Literal["+"] | Literal["*"] | Literal["||"]
        ] = SIMPLE_OPERATORS,
    ) -> bool:
        positions = len(self.values) - 1
        for operator_combination in itertools.product(operators, repeat=positions):
            total = self.values[0]
            for operator, next_value in zip(operator_combination, self.values[1:]):
                match operator:
                    case "+":
                        total += next_value
                    case "*":
                        total *= next_value
                    case "||":
                        total = concat_numbers(total, next_value)
            if total == self.test_value:
                return True
        return False

    def can_be_valid_complex(self) -> bool:
        return self.can_be_valid(operators=COMPLEX_OPERATORS)


def concat_numbers(a: int, b: int) -> int:
    b_tens = int(math.log10(b)) + 1
    offset_a = a * int(math.pow(10, b_tens))
    return offset_a + b


def part_one_answer(lines: list[str]):
    equations = map(Equation.parse, lines)
    return sum(e.test_value for e in equations if e.can_be_valid())


def part_two_answer(lines: list[str]):
    equations = [Equation.parse(l) for l in lines]
    with Pool() as p:
        results = p.map(Equation.can_be_valid_complex, equations)
    valid_equations = [e for (e, is_valid) in zip(equations, results) if is_valid]
    return sum(e.test_value for e in valid_equations)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day07input")
    print("Part One:", part_one_answer(puzzle_input))
    start = time.time()
    print("Part Two:", part_two_answer(puzzle_input))
    elapsed = time.time() - start
    print(f"part two took {elapsed} seconds")
