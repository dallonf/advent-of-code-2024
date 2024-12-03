from .day03 import (
    DoInstruction,
    DontInstruction,
    MulInstruction,
    extract_mul_instructions,
    extract_supported_instructions,
    part_one_answer,
    part_two_answer,
)

SAMPLE_INPUT = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


def test_extract_mul_instructions():
    result = extract_mul_instructions(SAMPLE_INPUT)
    assert result == [
        MulInstruction(2, 4),
        MulInstruction(5, 5),
        MulInstruction(11, 8),
        MulInstruction(8, 5),
    ]


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT) == 161


PART_TWO_SAMPLE_INPUT = (
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
)


def test_extract_all_instructions():
    result = extract_supported_instructions(PART_TWO_SAMPLE_INPUT)
    print(result)
    assert result == [
        MulInstruction(2, 4),
        DontInstruction(),
        MulInstruction(5, 5),
        MulInstruction(11, 8),
        DoInstruction(),
        MulInstruction(8, 5),
    ]

def test_part_two_answer():
    assert part_two_answer(PART_TWO_SAMPLE_INPUT) == 48