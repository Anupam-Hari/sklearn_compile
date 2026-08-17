from pathlib import Path

from transpiler.project.analyze import (
    analyze_project,
)

from transpiler.resolver.class_resolver import (
    resolve_classes,
)

graph = analyze_project(
    Path("sklearn/tree"),
)

resolve_classes(
    graph,
)

print("CLASS INHERITANCE")
print("=" * 80)

for child, parents in (
    graph.class_inheritance.items()
):

    print(
        child,
        "->",
        [
            parent.name
            for parent in parents
        ],
    )