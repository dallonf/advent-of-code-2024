from textwrap import dedent
import aoc2024.common.input as aoc_input
from .day24 import Device, part_one_answer

SMALL_INPUT = aoc_input.lines(
    dedent(
        """
        x00: 1
        x01: 1
        x02: 1
        y00: 0
        y01: 1
        y02: 0

        x00 AND y00 -> z00
        x01 XOR y01 -> z01
        x02 OR y02 -> z02
        """
    )
)
SAMPLE_INPUT = aoc_input.load_lines("day24sample")


def test_simulate():
    device = Device.parse(SMALL_INPUT)
    device.simulate()
    assert device.wires["z00"] == False
    assert device.wires["z01"] == False
    assert device.wires["z02"] == True


def test_output():
    device = Device.parse(SMALL_INPUT)
    device.simulate()
    assert device.extract_output() == 4


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT) == 2024
