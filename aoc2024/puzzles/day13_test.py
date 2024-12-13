from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input
from .day13 import Machine, OptimalPresses, parse_all, part_one_answer

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


def test_optimal_presses():
    result = MACHINES[0].get_optimal_presses()
    assert result and result == OptimalPresses(80, 40)
    assert result.cost == 280
    result = MACHINES[2].get_optimal_presses()
    assert result and result == OptimalPresses(38, 86)
    assert result.cost == 200


def test_no_result():
    assert MACHINES[1].get_optimal_presses() == None
    assert MACHINES[3].get_optimal_presses() == None


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT) == 480
