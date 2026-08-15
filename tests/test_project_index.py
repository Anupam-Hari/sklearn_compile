from pathlib import Path

from transpiler.project.index import build_project_index


graph = build_project_index(
    Path("sklearn/sklearn/tree")
)

for file in sorted(graph.files):

    print(
        graph.files[file]
    )