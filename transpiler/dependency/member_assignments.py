import re
from pathlib import Path


CLASS_PATTERN = re.compile(
    r"cdef\s+class\s+([A-Za-z_][A-Za-z0-9_]*)"
)

LOCAL_DECLARATION = re.compile(
    r"cdef\s+(.+?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|$)"
)

MEMBER_ASSIGNMENT = re.compile(
    r"self\.([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)"
)


def extract_member_assignments(
    path: Path,
    class_name: str,
):

    lines = path.read_text().splitlines()

    inside_class = False

    local_types = {}
    members = {}

    for line in lines:

        stripped = line.strip()

        class_match = CLASS_PATTERN.match(stripped)

        if class_match:

            inside_class = (
                class_match.group(1) == class_name
            )

            continue

        if not inside_class:
            continue

        declaration = LOCAL_DECLARATION.match(
            stripped
        )

        if declaration:

            local_types[
                declaration.group(2)
            ] = declaration.group(1)

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