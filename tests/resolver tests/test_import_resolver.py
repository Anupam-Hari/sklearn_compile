from pathlib import Path

from transpiler.project.analyze import analyze_project

from transpiler.resolver.import_resolver import (
    build_import_index,
    resolve_import_symbol,
)

graph = analyze_project(
    Path("sklearn"),
)

print(len(graph.files))

for path in graph.files:

    if "metrics" in str(path):

        print(path)

graph.import_index = build_import_index(
    graph,
)

print(
    Path(
        "sklearn/metrics/_dist_metrics.py"
    ) in graph.files
)

print(
    Path(
        "sklearn/metrics/_dist_metrics.pyx"
    ) in graph.files
)

print(
    Path(
        "sklearn/metrics/_dist_metrics.pxd"
    ) in graph.files
)

for path in graph.files:

    if "_dist_metrics" in str(path):

        print(path)

print()
print("IMPORT RESOLUTION")
print("=" * 80)

resolved = 0
unresolved = 0

for file_path, imports in graph.imports.items():

    if not imports:
        continue

    # print()
    # print(file_path)

    for imported in imports:

        symbol = resolve_import_symbol(
            graph,
            imported,
        )

        if symbol is not None:

            resolved += 1

            # print(
            #     f"✓ {imported.module}.{imported.name}"
            #     f" -> "
            #     f"{symbol.file_path}"
            # )

        else:

            unresolved += 1

            # print(
            #     f"✗ {imported.module}.{imported.name}"
            # )
            # source_file = graph.import_index.get(
            #     imported.module,
            # )

            # print(source_file)

    # print(
    #     graph.import_index.get(
    #         "sklearn.metrics._dist_metrics"
    #     )
    # )

    # print(
    #     graph.import_index.get(
    #         "sklearn.metrics._pairwise_distances_reduction._argkmin"
    #     )
    # )

print()
print("=" * 80)

print(
    f"Resolved: {resolved}"
)

print(
    f"Unresolved: {unresolved}"
)