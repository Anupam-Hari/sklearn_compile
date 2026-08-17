from pathlib import Path

from transpiler.project.analyze import (
    analyze_project,
)

from transpiler.resolver.class_resolver import (
    build_class_index,
)

from transpiler.resolver.inherited_member_resolver import (
    resolve_inherited_members,
)

graph = analyze_project(
    Path("sklearn/tree"),
)

graph.class_index = (
    build_class_index(
        graph,
    )
)

members = (
    resolve_inherited_members(
        graph,
    )
)

print()

print(
    "INHERITED METHODS"
)

print(
    "=" * 80
)

for cls, methods in (
    members.items()
):

    if methods:

        print()

        print(cls)

        for method in methods:

            print(
                f"    {method}"
            )