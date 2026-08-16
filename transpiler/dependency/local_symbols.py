import re


CDEF_PATTERN = re.compile(
    r"cdef\s+(.+?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|$)"
)


def extract_local_symbols(source: str):

    symbols = {}

    for line in source.splitlines():

        line = line.strip()

        if not line.startswith("cdef "):
            continue

        match = CDEF_PATTERN.match(line)

        if not match:
            continue

        variable_type = match.group(1).strip()

        variable_name = match.group(2).strip()

        symbols[variable_name] = variable_type

    return symbols