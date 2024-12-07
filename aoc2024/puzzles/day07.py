from dataclasses import dataclass
import itertools
import aoc2024.common.input as aoc_input

OPERATORS = ("+", "*")


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

    def can_be_valid(self) -> bool:
        positions = len(self.values) - 1
        for operator_combination in itertools.product(OPERATORS, repeat=positions):
            total = self.values[0]
            for operator, next_value in zip(operator_combination, self.values[1:]):
                match operator:
                    case "+":
                        total += next_value
                    case "*":
                        total *= next_value
                if total >= self.test_value:
                    # since both of the operators increase the value,
                    # there's no way to recover if we go over the test value
                    continue
            if total == self.test_value:
                return True
        return False


def part_one_answer(lines: list[str]):
    equations = map(Equation.parse, lines)
    return sum(e.test_value for e in equations if e.can_be_valid())


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day07input")
    print("Part One:", part_one_answer(puzzle_input))
