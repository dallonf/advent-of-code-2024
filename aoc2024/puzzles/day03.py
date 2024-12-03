from dataclasses import dataclass
import re
import aoc2024.common.input as aoc_input


@dataclass
class MulInstruction:
    a: int
    b: int

    def execute(self):
        return self.a * self.b


def extract_mul_instructions(program_memory: str) -> list[MulInstruction]:
    matches = re.findall(r"mul\(([0-9]+),([0-9+]+)\)", program_memory)
    result = [MulInstruction(int(m[0]), int(m[1])) for m in matches]
    return result


def part_one_answer(program_memory: str) -> int:
    instructions = extract_mul_instructions(program_memory)
    return sum(i.execute() for i in instructions)


if __name__ == "__main__":
    puzzle_input = aoc_input.load("day03input")

    print("Part One:", part_one_answer(puzzle_input))
