from pathlib import Path

from transpiler.project.analyze import analyze_project

from transpiler.resolver.import_resolver import (
    build_import_index,
    resolve_import_symbol,
)

graph = analyze_project(
    Path("sklearn"),
)

graph.import_index = build_import_index(
    graph,
)

print()
print("IMPORT RESOLUTION")
print("=" * 80)

resolved = 0
unresolved = 0

for file_path, imports in graph.imports.items():

    if not imports:
        continue

    print()
    print(file_path)

    for imported in imports:

        symbol = resolve_import_symbol(
            graph,
            imported,
        )

        if symbol is not None:

            resolved += 1

            print(
                f"✓ {imported.module}.{imported.name}"
                f" -> "
                f"{symbol.file_path}"
            )

        else:

            unresolved += 1

            print(
                f"✗ {imported.module}.{imported.name}"
            )
            source_file = graph.import_index.get(
                imported.module,
            )

            print(source_file)

print()
print("=" * 80)

print(
    f"Resolved: {resolved}"
)

print(
    f"Unresolved: {unresolved}"
)