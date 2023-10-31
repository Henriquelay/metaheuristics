def parse(path: str):
    """Parses a whole instance definition that lives in the system file path given."""

    from uctp.model import UCTP

    problem_instance = None
    with open(path) as file:
        lines = file.readlines()
        problem_instance = UCTP.parse(lines)
    file.close()
    return problem_instance


def keyword(line: str, keyword: str) -> str:
    """Parses a keyword from a line, removing it from the line."""

    if not line.startswith(keyword):
        raise Exception(f"Expected keyword `{keyword!r}` but found `{line[:len(keyword)]!r}`.")
    return line[len(keyword) :]


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
        raise Exception("Unexpected end of instance definition.")
    return None, ""
