from pathlib import Path

from transpiler.dependency.resolver import (
    build_dependency_tree,
)
from transpiler.project.analyze import analyze_project

graph = analyze_project(
    Path("sklearn"),
)

dependencies = build_dependency_tree(

    graph,

    Path(
        "sklearn/tree/_splitter.pyx",
    ),
)

print()

print("=" * 80)

print("RECURSIVE DEPENDENCIES")

print("=" * 80)

seen = set()

for dependency in dependencies:

    key = (
        dependency.name,
        dependency.file_path,
    )

    if key in seen:

        continue

    seen.add(
        key,
    )

    print(

        dependency.name,

        "->",

        dependency.file_path,
    )