import aoc2024.common.input as aoc_input
from aoc2024.puzzles.day23 import NetworkConnections

SAMPLE_INPUT = aoc_input.load_lines("day23sample")


def test_find_all_triads():
    connections = NetworkConnections.parse(SAMPLE_INPUT)
    triads = connections.find_all_triads()
    assert len(triads) == 12
    assert all(len(s) == 3 for s in triads)


def test_find_all_historian_triads():
    connections = NetworkConnections.parse(SAMPLE_INPUT)
    triads = connections.find_all_historian_triads()
    assert len(triads) == 7
