from textwrap import dedent
import aoc2024.common.input as aoc_input
from .day17 import Computer, part_two_answer


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
    assert part_two_answer(sample_input) == 117440
