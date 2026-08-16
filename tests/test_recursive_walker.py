from pathlib import Path

from transpiler.graph.recursive_walker import (
    walk_cython,
)
from transpiler.project.analyze import (
    analyze_project,
)


graph = analyze_project(
    Path("sklearn/sklearn/tree")
)

walk_cython(
    graph,
    "DepthFirstTreeBuilder",
    "build",
)