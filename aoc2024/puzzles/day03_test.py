from .day03 import MulInstruction, extract_mul_instructions, part_one_answer

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
