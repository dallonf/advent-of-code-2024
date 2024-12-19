import aoc2024.common.input as aoc_input
from .day19 import (
    parse,
    is_design_possible,
    part_one_answer,
    part_two_answer,
    possible_arrangements,
)

SAMPLE_INPUT_LINES = aoc_input.load_lines("day19sample")
SAMPLE_INPUT = parse(SAMPLE_INPUT_LINES)


def test_is_design_possible():
    patterns = SAMPLE_INPUT.patterns
    assert is_design_possible("brwrr", patterns)
    assert not is_design_possible("ubwu", patterns)


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT_LINES) == 6


def test_possible_arrangements():
    patterns = SAMPLE_INPUT.patterns
    assert possible_arrangements("brwrr", patterns) == 2


def test_part_two_answer():
    assert part_two_answer(SAMPLE_INPUT_LINES) == 16
