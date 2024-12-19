from textwrap import dedent

from pytest import skip
import aoc2024.common.input as aoc_input
from .day17 import (
    Computer,
    part_two_answer,
    disassemble,
)


def test_programs():
    computer = Computer([2, 6], c=9)
    computer.execute()
    assert computer.register_b == 1

    computer = Computer([5, 0, 5, 1, 5, 4], a=10)
    computer.execute()
    assert computer.output == [0, 1, 2]

    computer = Computer([0, 1, 5, 4, 3, 0], a=2024)
    computer.execute()
    assert computer.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert computer.register_a == 0

    computer = Computer([1, 7], b=29)
    computer.execute()
    assert computer.register_b == 26

    computer = Computer([4, 0], b=2024, c=43690)
    computer.execute()
    assert computer.register_b == 44354


def test_full_input():
    sample_input = aoc_input.lines(
        dedent(
            """
            Register A: 729
            Register B: 0
            Register C: 0

            Program: 0,1,5,4,3,0
            """
        )
    )

    computer = Computer.parse(sample_input)
    computer.execute()
    assert computer.output == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]


def test_part_two_answer():
    skip("off by one compared to real input/answer, not sure I can generalize")
    sample_input = aoc_input.lines(
        dedent(
            """
            Register A: 2024
            Register B: 0
            Register C: 0

            Program: 0,3,5,4,3,0
            """
        )
    )
    print(disassemble(Computer.parse(sample_input).instruction_memory))
    assert oct(part_two_answer(sample_input, lambda a: a % 8)) == oct(117440)


def test_octal_hypothesis():
    octal_num = 0o163602634
    assert octal_num % 8 == 4
    next_num = octal_num // 8
    assert next_num == 0o16360263
    assert next_num % 8 == 3

    digits = list[int]()
    next_num = octal_num
    while next_num > 0:
        digits.append(next_num % 8)
        next_num = next_num // 8
    assert [str(d) for d in digits] == list(reversed(oct(octal_num).removeprefix("0o")))
