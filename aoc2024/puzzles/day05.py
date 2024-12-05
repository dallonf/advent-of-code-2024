from dataclasses import dataclass
import re
import aoc2024.common.input as aoc_input


@dataclass(frozen=True, eq=True)
class OrderRule:
    before: int
    after: int

    def is_relevant(self, page: int) -> bool:
        return page == self.before or page == self.after

    @staticmethod
    def parse(line: str) -> "OrderRule":
        match = re.match(r"([0-9]+)\|([0-9]+)", line)
        assert match != None, f"{line} is not a valid format"
        return OrderRule(int(match.group(1)), int(match.group(2)))


@dataclass(frozen=True, eq=True)
class Ruleset:
    rules: list[OrderRule]


@dataclass(frozen=True, eq=True)
class Update:
    pages: list[int]

    @staticmethod
    def parse(line: str) -> "Update":
        numbers = line.split(",")
        return Update([int(n) for n in numbers])


@dataclass(frozen=True, eq=True)
class PuzzleInput:
    ruleset: Ruleset
    updates: list[Update]

    @staticmethod
    def parse(lines: list[str]) -> "PuzzleInput":

        rule_lines = lines[: lines.index("")]
        update_lines = lines[lines.index("") + 1 :]

        rules = [OrderRule.parse(l) for l in rule_lines]
        updates = [Update.parse(l) for l in update_lines]

        return PuzzleInput(ruleset=Ruleset(rules), updates=updates)


if __name__ == "__main__":
    puzzle_input = aoc_input.load_lines("day05input")
