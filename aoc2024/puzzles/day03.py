from dataclasses import dataclass
import re
import aoc2024.common.input as aoc_input


@dataclass
class MulInstruction:
    a: int
    b: int

    def execute(self):
        return self.a * self.b


@dataclass
class DoInstruction:
    pass


@dataclass
class DontInstruction:
    pass


type Instruction = MulInstruction | DoInstruction | DontInstruction


def extract_mul_instructions(program_memory: str) -> list[MulInstruction]:
    matches = re.findall(r"mul\(([0-9]+),([0-9+]+)\)", program_memory)
    result = [MulInstruction(int(m[0]), int(m[1])) for m in matches]
    return result


def extract_supported_instructions(program_memory: str) -> list[Instruction]:
    matches = re.findall(r"(do|don't|mul)\(([0-9,]*)\)", program_memory)
    result: list[Instruction] = []
    for m in matches:
        if m[0] == "mul":
            params = re.match(r"([0-9]+),([0-9+]+)", m[1])
            if params != None:
                result.append(
                    MulInstruction(int(params.group(1)), int(params.group(2)))
                )
        elif m[0] == "do" and m[1] == "":
            result.append(DoInstruction())
        elif m[0] == "don't" and m[1] == "":
            result.append(DontInstruction())
    return result


def part_one_answer(program_memory: str) -> int:
    instructions = extract_mul_instructions(program_memory)
    return sum(i.execute() for i in instructions)


def part_two_answer(program_memory: str) -> int:
    instructions = extract_supported_instructions(program_memory)
    result = 0
    enabled = True
    for instruction in instructions:
        match instruction:
            case MulInstruction():
                if enabled:
                    result += instruction.execute()
            case DoInstruction():
                enabled = True
            case DontInstruction():
                enabled = False
    return result


if __name__ == "__main__":
    puzzle_input = aoc_input.load("day03input")

    print("Part One:", part_one_answer(puzzle_input))
    print("Part Two:", part_two_answer(puzzle_input))
