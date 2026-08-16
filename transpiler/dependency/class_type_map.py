from pathlib import Path

from transpiler.dependency.class_members import (
    extract_member_assignments,
)

from transpiler.dependency.type_normalizer import (
    normalize_type,
)


def build_class_type_map(
    path: Path,
    class_name: str,
):

    members = extract_member_assignments(
        path,
        class_name,
    )

    return {
        name: normalize_type(member_type)
        for name, member_type in members.items()
    }