import re
from pathlib import Path


CLASS_PATTERN = re.compile(
    r"cdef\s+class\s+([A-Za-z_][A-Za-z0-9_]*)"
)

PARAMETER_PATTERN = re.compile(
    r"(.+)\s+([A-Za-z_][A-Za-z0-9_]*)$"
)


def extract_constructor_parameters(
    path: Path,
    class_name: str,
):

    lines = path.read_text().splitlines()

    inside_class = False
    inside_constructor = False

    parameters = {}

    for line in lines:

        stripped = line.strip()

        class_match = CLASS_PATTERN.match(
            stripped
        )

        if class_match:

            inside_class = (
                class_match.group(1)
                == class_name
            )

            inside_constructor = False

            continue

        if not inside_class:
            continue

        if stripped.startswith(
            "def __cinit__("
        ):

            inside_constructor = True

            continue

        if not inside_constructor:
            continue

        if stripped == "):":

            break

        if (
            not stripped
            or stripped == "self,"
        ):

            continue

        parameter = stripped.rstrip(",")

        match = PARAMETER_PATTERN.match(
            parameter
        )

        if match:

            parameters[
                match.group(2)
            ] = match.group(1)

    return parameters