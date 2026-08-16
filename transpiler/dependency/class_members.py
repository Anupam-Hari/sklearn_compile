import re
from pathlib import Path

from transpiler.dependency.constructor_parameters import (
    extract_constructor_parameters,
)


CLASS_PATTERN = re.compile(
    r"cdef\s+class\s+([A-Za-z_][A-Za-z0-9_]*)"
    r"(?:\(([A-Za-z_][A-Za-z0-9_]*)\))?"
)

LOCAL_DECLARATION = re.compile(
    r"cdef\s+(.+?)\s+(.+)$"
)

MEMBER_ASSIGNMENT = re.compile(
    r"self\.([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)"
)

def extract_member_assignments(
    path: Path,
    class_name: str,
):

    lines = path.read_text().splitlines()

    local_types = extract_constructor_parameters(
        path,
        class_name,
    )

    members = {}

    inside_class = False

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

            continue

        if not inside_class:
            continue

        declaration = LOCAL_DECLARATION.match(
            stripped
        )

        if declaration:

            declared_type = (
                declaration.group(1)
                .strip()
            )

            variables = (
                declaration.group(2)
                .split(",")
            )

            for variable in variables:

                variable = (
                    variable
                    .strip()
                    .split("=")[0]
                    .strip()
                )

                if variable:

                    local_types[
                        variable
                    ] = declared_type

            continue

        assignment = MEMBER_ASSIGNMENT.match(
            stripped
        )

        if not assignment:
            continue

        member = assignment.group(1)

        value = assignment.group(2).strip()

        if value.endswith(" is not None"):

            members[member] = "bint"

        elif value in ("True", "False"):

            members[member] = "bint"

        elif value in local_types:

            members[member] = local_types[value]

    return members