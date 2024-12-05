from .day05 import OrderRule, PuzzleInput, Update
import aoc2024.common.input as aoc_input

SAMPLE_INPUT = aoc_input.load_lines("day05sample")


class TestPuzzleInput:
    def test_parse(self):
        result = PuzzleInput.parse(SAMPLE_INPUT)
        assert len(result.ruleset.rules) == 21
        assert result.ruleset.rules[0] == OrderRule(47, 53)
        assert result.ruleset.rules[1] == OrderRule(97, 13)
        assert result.ruleset.rules[2] == OrderRule(97, 61)

        assert len(result.updates) == 6
        assert result.updates[0] == Update([75, 47, 61, 53, 29])
        assert result.updates[1] == Update([97, 61, 53, 29, 13])
        assert result.updates[2] == Update([75, 29, 13])
