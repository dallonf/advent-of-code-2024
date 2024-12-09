from .day09 import FileSystem


class TestFileSystem:
    def test_parse(self):
        assert FileSystem.parse("12345").debug() == "0..111....22222"
        assert (
            FileSystem.parse("2333133121414131402").debug()
            == "00...111...2...333.44.5555.6666.777.888899"
        )

    def test_defrag(self):
        file_system = FileSystem.parse("12345")
        file_system.defrag()
        assert file_system.debug() == "022111222......"

        file_system = FileSystem.parse("2333133121414131402")
        file_system.defrag()
        assert file_system.debug() == "0099811188827773336446555566.............."

    def test_checksum(self):
        file_system = FileSystem.parse("2333133121414131402")
        file_system.defrag()
        assert file_system.checksum() == 1928
