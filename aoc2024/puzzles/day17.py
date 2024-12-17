from enum import Enum, auto
import aoc2024.common.input as aoc_input


class Register(Enum):
    A = auto()
    B = auto()
    C = auto()


class Computer:
    instruction_memory: list[int]
    register_a: int
    register_b: int
    register_c: int
    instruction_pointer: int

    output: list[int]

    def __init__(self, instructions: list[int], /, a: int = 0, b: int = 0, c: int = 0):
        self.instruction_memory = instructions
        self.register_a = a
        self.register_b = b
        self.register_c = c

        self.output = list[int]()
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


def part_one_answer(lines: list[str]) -> str:
    computer = Computer.parse(lines)
    computer.execute()
    return ",".join((str(o) for o in computer.output))


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day17input")
    print("Part One:", part_one_answer(puzzle_input))
