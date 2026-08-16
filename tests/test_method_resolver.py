from pathlib import Path

from transpiler.cython.method_resolver import (
    resolve_cython_method,
)
from transpiler.project.analyze import (
    analyze_project,
)


graph = analyze_project(
    Path("sklearn/sklearn/tree")
)

method = resolve_cython_method(
    graph,
    "DepthFirstTreeBuilder",
    "build",
)

print(method)