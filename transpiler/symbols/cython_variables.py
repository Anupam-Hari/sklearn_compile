import re


VARIABLE_PATTERN = re.compile(
    r"cdef\s+(.+?)\s+([A-Za-z_][A-Za-z0-9_]*)"
)


def extract_variables(source: str):

    variables = []

    for line in source.splitlines():

        line = line.strip()

        if not line.startswith("cdef "):
            continue

        match = VARIABLE_PATTERN.match(line)

        if not match:
            continue

        variables.append(
            (
                match.group(2),
                match.group(1),
            )
        )

    return variables