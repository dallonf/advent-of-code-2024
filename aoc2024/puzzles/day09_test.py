from .day09 import FileSystem, part_one_answer


class TestFileSystem:
    def test_parse(self):
        assert FileSystem.parse("12345").debug() == "0..111....22222"
        assert (
            FileSystem.parse("2333133121414131402").debug()
            == "00...111...2...333.44.5555.6666.777.888899"
        )

    def test_compact(self):
        file_system = FileSystem.parse("12345")
        file_system.compact()
        assert file_system.debug() == "022111222......"

        file_system = FileSystem.parse("2333133121414131402")
        file_system.compact()
        assert file_system.debug() == "0099811188827773336446555566.............."

        file_system = FileSystem.parse("90909")
        file_system.compact()
        assert file_system.debug() == "000000000111111111222222222"

        file_system = FileSystem.parse("25441")
        assert file_system.debug() == "00.....1111....2"
        file_system.compact()
        assert file_system.debug() == "0021111........."

    def test_checksum(self):
        file_system = FileSystem.parse("2333133121414131402")
        file_system.compact()
        assert file_system.checksum() == 1928


def test_part_one_answer():
    result = part_one_answer("2333133121414131402")
    assert result == 1928


def test_edge_cases():
    assert part_one_answer("1010101010101010101010") == 385
    assert part_one_answer("12345") == 60
    assert part_one_answer("252") == 5
    assert (
        part_one_answer("90909") == FileSystem.parse("90909").checksum()
    )  # nothing to compact here
