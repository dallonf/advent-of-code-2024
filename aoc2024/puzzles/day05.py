from dataclasses import dataclass
from functools import cache, cached_property
import re
import aoc2024.common.input as aoc_input


@dataclass(frozen=True, eq=True)
class OrderRule:
    before: int
    after: int

    @staticmethod
    def parse(line: str) -> "OrderRule":
        match = re.match(r"([0-9]+)\|([0-9]+)", line)
        assert match != None, f"{line} is not a valid format"
        return OrderRule(int(match.group(1)), int(match.group(2)))

    def is_relevant(self, update: "Update") -> bool:
        return self.before in update.pages and self.after in update.pages

    def check_compliance(self, update: "Update") -> bool:
        if not self.is_relevant(update):
            return True

        before_idx = update.pages.index(self.before)
        after_idx = update.pages.index(self.after)

        return before_idx < after_idx


@dataclass(frozen=True, eq=True)
class Ruleset:
    rules: list[OrderRule]

    def check_compliance(self, update: "Update") -> bool:
        return all((r.check_compliance(update) for r in self.rules))


@dataclass(frozen=True, eq=True)
class Update:
    pages: list[int]

    @staticmethod
    def parse(line: str) -> "Update":
        numbers = line.split(",")
        return Update([int(n) for n in numbers])

    @cached_property
    def middle_page(self):
        assert (
            len(self.pages) % 2 == 1
        ), f"Update has {len(self.pages)} pages; can only get the middle page for an odd number"
        return self.pages[len(self.pages) // 2]

    def reorder(self, ruleset: Ruleset) -> "Update":
        relevant_rules: list[OrderRule] = [
            r for r in ruleset.rules if r.is_relevant(self)
        ]

        @cache
        def get_all_prerequisites(page: int) -> set[int]:
            result: set[int] = set()
            for rule in relevant_rules:
                if rule.after == page:
                    result.add(rule.before)
                    result = result.union(get_all_prerequisites(rule.before))
            return result

        new_pages: list[int] = []
        while len(new_pages) < len(self.pages):
            plausible_next_items = [
                page
                for page in self.pages
                if page not in new_pages
                and len(get_all_prerequisites(page).difference(new_pages)) == 0
            ]
            new_pages.append(plausible_next_items[0])

        return Update(new_pages)


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

    def part_one_answer(self):
        compliant_updates = [
            u for u in self.updates if self.ruleset.check_compliance(u)
        ]
        return sum((u.middle_page for u in compliant_updates))

    def part_two_answer(self):
        incorrectly_ordered_updates = [
            u for u in self.updates if not self.ruleset.check_compliance(u)
        ]
        fixed_updates = [u.reorder(self.ruleset) for u in incorrectly_ordered_updates]
        return sum(u.middle_page for u in fixed_updates)


if __name__ == "__main__":
    puzzle_input = PuzzleInput.parse(aoc_input.load_lines("day05input"))
    print("Part One:", puzzle_input.part_one_answer())
    print("Part Two:", puzzle_input.part_two_answer())
