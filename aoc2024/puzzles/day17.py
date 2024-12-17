from dataclasses import dataclass
from enum import Enum, auto
import itertools
from typing import Optional
import aoc2024.common.input as aoc_input


class Register(Enum):
    A = auto()
    B = auto()
    C = auto()


@dataclass(frozen=True)
class ComputerState:
    instruction_pointer: int
    register_a: int
    register_b: int
    register_c: int


class Computer:
    instruction_memory: list[int]
    register_a: int
    register_b: int
    register_c: int
    instruction_pointer: int

    output: list[int]

    def __init__(
        self,
        instructions: list[int],
        /,
        a: int = 0,
        b: int = 0,
        c: int = 0,
        cache: Optional[dict[ComputerState, list[int]]] = None,
    ):
        self.instruction_memory = instructions
        self.register_a = a
        self.register_b = b
        self.register_c = c

        self.output = list[int]()
        self.cache = cache or dict()
        self.instruction_pointer = 0

    @staticmethod
    def parse(lines: list[str]):
        assert len(lines) == 5
        a = int(lines[0].split(": ")[1])
        b = int(lines[1].split(": ")[1])
        c = int(lines[2].split(": ")[1])

        program = [int(n) for n in lines[4].split(": ")[1].split(",")]
        return Computer(program, a=a, b=b, c=c)

    def read_register(self, register: Register) -> int:
        match register:
            case Register.A:
                return self.register_a
            case Register.B:
                return self.register_b
            case Register.C:
                return self.register_c

    def write_register(self, register: Register, value: int):
        match register:
            case Register.A:
                self.register_a = value
            case Register.B:
                self.register_b = value
            case Register.C:
                self.register_c = value

    def read_combo_operand(self, value: int) -> int:
        match value:
            case 0 | 1 | 2 | 3:
                return value
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case _:
                raise AssertionError(f"Unexpected combo operand: {value}")

    def execute_instruction(self, instruction: int, operand: int):
        match instruction:
            case 0:  # ADV: A Divide Value
                result = self.register_a // pow(2, self.read_combo_operand(operand))
                self.register_a = result
            case 1:  # BXL: B XOR Literal
                result = self.register_b ^ operand
                self.register_b = result
            case 2:  # BST: B SeT
                result = self.read_combo_operand(operand) % 8
                self.register_b = result
            case 3:  # JNZ: Jump Not Zero
                if self.register_a != 0:
                    # note that 2 will always be added after
                    # executing an instruction
                    # just hackily offset by that
                    self.instruction_pointer = operand - 2
            case 4:  # BXC: B XOR C
                result = self.register_b ^ self.register_c
                self.register_b = result
            case 5:  # OUT: Output
                result = self.read_combo_operand(operand) % 8
                self.output.append(result)
            case 6:  # BDV: B Divide Value
                result = self.register_a // pow(2, self.read_combo_operand(operand))
                self.register_b = result
            case 7:  # CDV: C Divide Value
                result = self.register_a // pow(2, self.read_combo_operand(operand))
                self.register_c = result
            case _:
                raise AssertionError(f"Unexpected opcode: {instruction}")

    def execute(self):
        while self.instruction_pointer < len(self.instruction_memory):
            self.execute_instruction(
                self.instruction_memory[self.instruction_pointer],
                self.instruction_memory[self.instruction_pointer + 1],
            )
            self.instruction_pointer += 2

    # actually slower than just `execute`
    def execute_searching(self, expected_output: list[int]) -> bool:
        explored_states = list[tuple[ComputerState, list[int]]]()
        while self.instruction_pointer < len(self.instruction_memory):
            current_state = ComputerState(
                self.instruction_pointer,
                self.register_a,
                self.register_b,
                self.register_c,
            )
            if current_state in self.cache:
                self.output += self.cache[current_state]
                break

            explored_states.append((current_state, list()))

            instruction = self.instruction_memory[self.instruction_pointer]
            operand = self.instruction_memory[self.instruction_pointer + 1]
            self.execute_instruction(instruction, operand)
            self.instruction_pointer += 2
            # if something was just outputted, add it to the cache
            if instruction == 5:
                for _, cached_output in explored_states:
                    cached_output.append(self.output[-1])
        return self.output == expected_output


def disassemble_combo_operand(operand: int) -> str:
    match operand:
        case 0 | 1 | 2 | 3:
            return str(operand)
        case 4:
            return "A"
        case 5:
            return "B"
        case 6:
            return "C"
        case _:
            raise AssertionError(f"Unexpected combo operand: {operand}")


def disassemble_low_level_instruction(instruction: int, operand: int) -> str:
    match instruction:
        case 0:
            return f"adv {disassemble_combo_operand(operand)}"
        case 1:
            return f"bxl {operand}"
        case 2:
            return f"bst {disassemble_combo_operand(operand)}"
        case 3:
            return f"jnz {operand}"
        case 4:
            return "bxc"
        case 5:
            return f"out {disassemble_combo_operand(operand)}"
        case 6:
            return f"bdv {disassemble_combo_operand(operand)}"
        case 7:
            return f"cdv {disassemble_combo_operand(operand)}"
        case _:
            raise AssertionError(f"Unexpected opcode: {instruction}")


def disassemble_high_level_instruction(instruction: int, operand: int) -> str:
    match instruction:
        case 0:
            return f"A = A / pow(2, {disassemble_combo_operand(operand)})"
        case 1:
            return f"B = xor(B, {operand})"
        case 2:
            return f"B = {disassemble_combo_operand(operand)} % 8"
        case 3:
            return f"goto {operand} if A != 0"
        case 4:
            return "B = xor(B, C)"
        case 5:
            return f"output({disassemble_combo_operand(operand)} % 8)"
        case 6:
            return f"B = A / pow(2, {disassemble_combo_operand(operand)})"
        case 7:
            return f"C = A / pow(2, {disassemble_combo_operand(operand)})"
        case _:
            raise AssertionError(f"Unexpected opcode: {instruction}")


def disassemble(instructions: list[int]) -> str:
    pairs = itertools.batched(instructions, 2)
    lines = [
        f"{str(i).rjust(2)}: {disassemble_low_level_instruction(inst, op).ljust(5)} -- {disassemble_high_level_instruction(inst, op)}"
        for i, (inst, op) in enumerate(pairs)
    ]
    return "\n".join(lines)


def part_one_answer(lines: list[str]) -> str:
    computer = Computer.parse(lines)
    computer.execute()
    return ",".join((str(o) for o in computer.output))


def part_two_answer_overengineered_and_slow(lines: list[str]) -> int:
    prev_cache = None
    for candidate_a in range(1_000_000):
        computer = Computer.parse(lines)
        if prev_cache is not None:
            computer.cache = prev_cache
        computer.register_a = candidate_a
        success = computer.execute_searching(computer.instruction_memory)
        prev_cache = computer.cache
        if success:
            return candidate_a
    raise AssertionError("No candidate found in 0 - 1,000,000")


def part_two_answer(lines: list[str]) -> int:
    for candidate_a in range(1_000_000):
        computer = Computer.parse(lines)
        computer.register_a = candidate_a
        computer.execute()
        if computer.output == computer.instruction_memory:
            return candidate_a
    raise AssertionError("No candidate found in 0 - 1,000,000")


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day17input")
    puzzle_instructions = Computer.parse(puzzle_input).instruction_memory
    print("Disassembly:")
    print(disassemble(puzzle_instructions))
    print("Part One:", part_one_answer(puzzle_input))
    # not yet optimized enough to run
    # print("Part Two:", part_two_answer(puzzle_input))
