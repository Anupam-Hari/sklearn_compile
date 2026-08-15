from pathlib import Path

from transpiler.dependency.models import (
    DependencyGraph,
    SourceFile,
)


def build_project_index(root: Path) -> DependencyGraph:

    graph = DependencyGraph()

    extensions = {
        ".py": "python",
        ".pyx": "cython",
        ".pxd": "cython",
        ".pxi": "cython",
    }

    for path in root.rglob("*"):

        if path.suffix not in extensions:
            continue

        graph.files[path] = SourceFile(
            path=path,
            extension=path.suffix,
            language=extensions[path.suffix],
        )

    return graph