from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input
from aoc2024.puzzles.day13 import Machine, parse_all

SAMPLE_INPUT = aoc_input.load_lines("day13sample")
MACHINES = parse_all(SAMPLE_INPUT)


def test_parse_all():
    results = parse_all(SAMPLE_INPUT)
    assert len(results) == 4
    assert results[0] == Machine(
        button_a=IntVector2(94, 34),
        button_b=IntVector2(22, 67),
        prize=IntVector2(8400, 5400),
    )
    assert results[3] == Machine(
        button_a=IntVector2(69, 23),
        button_b=IntVector2(27, 71),
        prize=IntVector2(18641, 10279),
    )
