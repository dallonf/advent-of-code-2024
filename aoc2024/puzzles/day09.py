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

    def defrag(self):
        blocks = self.blocks
        first_available_space = blocks.index(None)
        for idx, file_id in reversed(list(enumerate(blocks))):
            if file_id == None:
                continue
            assert blocks[first_available_space] == None
            blocks[first_available_space] = file_id
            blocks[idx] = None
            try:
                first_available_space = blocks.index(
                    None, first_available_space, idx - 1
                )
            except ValueError:
                # done
                break

    def checksum(self):
        return sum((b * i for i, b in enumerate(self.blocks) if b != None))


def part_one_answer(line: str):
    filesystem = FileSystem.parse(line)
    filesystem.defrag()
    return filesystem.checksum()


if __name__ == "__main__":
    puzzle_input = aoc_input.load("day09input").rstrip()
    # too high: 6337367227720
    print("Part One:", part_one_answer(puzzle_input))