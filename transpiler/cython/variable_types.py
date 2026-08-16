import re
from pathlib import Path


VARIABLE_PATTERN = re.compile(
    r"cdef\s+([A-Za-z_][A-Za-z0-9_]*(?:\[[^\]]+\])?)\s+([A-Za-z_][A-Za-z0-9_]*)"
)


def extract_variable_types(path: Path) -> dict[str, str]:

    source = path.read_text()

    variables = {}

    for match in VARIABLE_PATTERN.finditer(source):

        variable_type = match.group(1)

        variable_name = match.group(2)

        if "[" in variable_type:
            variable_type = variable_type.split("[")[-1].rstrip("]")

        variables[variable_name] = variable_type

    return variables