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

    def test_part_one_answer(self):
        puzzle_input = PuzzleInput.parse(SAMPLE_INPUT)
        assert puzzle_input.part_one_answer() == 143

    def test_part_two_answer(self):
        puzzle_input = PuzzleInput.parse(SAMPLE_INPUT)
        assert puzzle_input.part_two_answer() == 123


class TestUpdate:
    def test_is_valid(self):
        puzzle_input = PuzzleInput.parse(SAMPLE_INPUT)
        assert puzzle_input.ruleset.check_compliance(puzzle_input.updates[0]) == True
        assert puzzle_input.ruleset.check_compliance(puzzle_input.updates[1]) == True
        assert puzzle_input.ruleset.check_compliance(puzzle_input.updates[2]) == True
        assert puzzle_input.ruleset.check_compliance(puzzle_input.updates[3]) == False
        assert puzzle_input.ruleset.check_compliance(puzzle_input.updates[4]) == False
        assert puzzle_input.ruleset.check_compliance(puzzle_input.updates[5]) == False

    def test_middle_page(self):
        puzzle_input = PuzzleInput.parse(SAMPLE_INPUT)
        updates = puzzle_input.updates
        assert updates[0].middle_page == 61
        assert updates[1].middle_page == 53
        assert updates[2].middle_page == 29

    def test_reorder(self):
        ruleset = PuzzleInput.parse(SAMPLE_INPUT).ruleset
        assert Update([75, 97, 47, 61, 53]).reorder(ruleset) == Update(
            [97, 75, 47, 61, 53]
        )
        assert Update([61, 13, 29]).reorder(ruleset) == Update([61, 29, 13])
        assert Update([97, 13, 75, 29, 47]).reorder(ruleset) == Update(
            [97, 75, 47, 29, 13]
        )
