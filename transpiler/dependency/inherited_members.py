from transpiler.dependency.class_members import (
    extract_member_assignments,
)

from transpiler.dependency.resolver import (
    find_symbol,
)


def get_all_class_members(
    graph,
    class_name,
):

    symbol = find_symbol(
        graph,
        class_name,
    )

    print()
    print("CLASS:", class_name)

    members = extract_member_assignments(
        symbol.file_path,
        class_name,
    )

    print("DIRECT:", members)

    if symbol.base_class:

        inherited = get_all_class_members(
            graph,
            symbol.base_class,
        )

        inherited.update(
            members,
        )

        return inherited

    return members