from dataclasses import dataclass
import itertools
import aoc2024.common.input as aoc_input


@dataclass
class FileSystem:
    blocks: list[int | None]

    @staticmethod
    def parse(line: str) -> "FileSystem":
        char_pairs = itertools.batched(line, 2, strict=False)
        blocks = list[int | None]()
        for i, pair in enumerate(char_pairs):
            size = int(pair[0])
            if len(pair) == 2:
                free_space = int(pair[1])
            else:
                free_space = 0
            for _ in range(size):
                blocks.append(i)
            for _ in range(free_space):
                blocks.append(None)
        return FileSystem(blocks)

    def copy(self) -> "FileSystem":
        return FileSystem(self.blocks.copy())

    def debug(self) -> str:
        if any((b != None and b > 10 for b in self.blocks)):
            raise AssertionError(
                "Can't debug display a filesystem with more than 9 files [the ID must take up only a single character]"
            )
        chars = ["." if b == None else str(b) for b in self.blocks]
        return "".join(chars)

    def debug_large(self) -> str:
        chars = ["." if b == None else str(b) for b in self.blocks]
        return " ".join(chars)

    def compact(self):
        blocks = self.blocks
        try:
            first_available_space = blocks.index(None)
        except ValueError:
            # no free space, can't compact
            return
        for idx, file_id in reversed(list(enumerate(blocks))):
            if file_id == None:
                continue
            if first_available_space > idx:
                # TODO: I've never been able to find a small test case
                # where this gets hit, but it's absolutely essential for
                # real input
                break

            blocks[first_available_space] = file_id
            blocks[idx] = None
            try:
                first_available_space = blocks.index(
                    None, first_available_space + 1, idx - 1
                )
            except ValueError:
                # done; no more free space
                break

    def checksum(self):
        return sum((b * i for i, b in enumerate(self.blocks) if b != None))


def part_one_answer(line: str):
    filesystem = FileSystem.parse(line)
    filesystem.compact()
    return filesystem.checksum()


if __name__ == "__main__":
    puzzle_input = aoc_input.load("day09input").rstrip()
    print("Part One:", part_one_answer(puzzle_input))
