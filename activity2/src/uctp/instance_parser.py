"""Atomic element parsing for the UCTP instance definition."""


from typing import Sequence


def parse_file(path: str):
    """Parses a whole instance definition that lives in the system file path given."""
    # This avoids circular imports
    from uctp.model import UCTP  # pylint: disable=import-outside-toplevel

    problem_instance = None
    with open(path, encoding="utf8") as file:
        lines = file.readlines()
        problem_instance = UCTP.parse(lines)
    file.close()
    return problem_instance


def skip_white_lines(body: Sequence[str]) -> Sequence[str]:
    """Removes all white lines from the beginning of the body."""

    while body[0].isspace() or body[0] == "":
        body = body[1:]
    return body


def keyword(line: str, tag: str) -> str:
    """Parses a keyword from a line, removing it from the line."""

    if not line.startswith(tag):
        raise ValueError(f"Expected keyword {tag!r} but found {line[:len(tag)]!r}.")
    return line[len(tag) :]


def parse_word(line: str) -> tuple[str, str]:
    """Parses a single word from a line, removing it from the line. A word is defined by a sequence of any non-whitespace characters."""

    word = ""
    while line and not line[0].isspace():
        word += line[0]
        line = line[1:]
    return word, line.lstrip()


def parse_int(line: str) -> tuple[int, str]:
    """Parses a single integer from a line, removing it from the line. A word is defined by a sequence of non-whitespace alphanumeric characters."""

    word, line = parse_word(line)
    return int(word), line


def parse_end(line: str) -> tuple[None, str]:
    """Parses the end of the instance definition."""

    if line != "END.":
        raise ValueError("Unexpected end of instance definition.")
    return None, ""
