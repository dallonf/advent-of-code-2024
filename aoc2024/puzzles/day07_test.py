from textwrap import dedent
import aoc2024.common.input as aoc_input
from .day07 import Equation, concat_numbers, part_one_answer, part_two_answer

SAMPLE_INPUT = aoc_input.lines(
    dedent(
        """
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
        """
    )
)


def test_parse():
    assert Equation.parse("190: 10 19") == Equation(190, [10, 19])
    assert Equation.parse("3267: 81 40 27") == Equation(3267, [81, 40, 27])


def test_can_be_valid():
    assert Equation.parse("190: 10 19").can_be_valid()
    assert Equation.parse("3267: 81 40 27").can_be_valid()
    assert not Equation.parse("83: 17 5").can_be_valid()
    assert not Equation.parse("156: 15 6").can_be_valid()
    assert Equation.parse("292: 11 6 16 20").can_be_valid()


def test_part_one_answer():
    result = part_one_answer(SAMPLE_INPUT)
    assert result == 3749


def test_complex_can_be_valid():
    assert Equation.parse("156: 15 6").can_be_valid_complex()
    assert Equation.parse("7290: 6 8 6 15").can_be_valid_complex()
    assert Equation.parse("192: 17 8 14").can_be_valid_complex()
    assert not Equation.parse("83: 17 5").can_be_valid_complex()
    assert not Equation.parse("161011: 16 10 13").can_be_valid_complex()


def test_concat_numbers():
    assert concat_numbers(12, 34) == 1234


def test_part_two_answer():
    result = part_two_answer(SAMPLE_INPUT)
    assert result == 11387
