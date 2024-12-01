from pathlib import Path


PUZZLES_DIR = (Path(__file__) / "../../puzzles").resolve()


def load(name: str, *_: None, parent_dir: Path = PUZZLES_DIR) -> str:
    with open(parent_dir / f"{name}.txt", encoding="utf-8") as f:
        return f.read()


def lines(
    file_contents: str,
    *_: None,
    trim_eof_line: bool = True,
    trim_starting_blank_line: bool = True,
) -> list[str]:
    """Split file contents into a list of lines.

    Args:
        file_contents (str)
        trim_eof_line (bool, optional): Removes a blank trailing newline. Defaults to True.
        trim_starting_blank_line (bool, optional): Removes a blank line at the very beginning. Useful for multiline strings. Defaults to True.
    """
    result = file_contents.splitlines()
    if trim_eof_line and result[-1] == "":
        result.pop()
    if trim_starting_blank_line and result[0] == "":
        result.remove("")
    return result


def load_lines(
    name: str,
    *_: None,
    parent_dir: Path = load.__kwdefaults__["parent_dir"],
    trim_eof_line: bool = lines.__kwdefaults__["trim_eof_line"],
    trim_starting_blank_line: bool = lines.__kwdefaults__["trim_starting_blank_line"],
):
    """Loads a file and splits it into a list of lines. Equivalent to calling input.load() and then input.lines()

    Args:
        file_contents (str)
        parent_dir (Path, optional)
        trim_eof_line (bool, optional): Removes a blank trailing newline. Defaults to True.
        trim_starting_blank_line (bool, optional): Removes a blank line at the very beginning. Defaults to True.
    """

    contents = load(name, parent_dir=parent_dir)
    result = lines(
        contents,
        trim_eof_line=trim_eof_line,
        trim_starting_blank_line=trim_starting_blank_line,
    )
    return result
