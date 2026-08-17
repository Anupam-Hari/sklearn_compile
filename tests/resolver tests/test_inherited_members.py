from pathlib import Path

from transpiler.project.analyze import (
    analyze_project,
)

from transpiler.resolver.class_resolver import (
    resolve_classes,
)

from transpiler.resolver.inherited_member_resolver import (
    resolve_inherited_members,
)

graph = analyze_project(
    Path("sklearn/tree"),
)

resolve_classes(
    graph,
)

resolve_inherited_members(
    graph,
)

print()

print(
    "INHERITED METHODS"
)

print(
    "=" * 80
)

for cls, methods in (
    graph.inherited_members.items()
):

    if not methods:

        continue

    print()

    print(cls)

    for method in methods:

        print(
            f"    {method}"
        )