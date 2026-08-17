from pathlib import Path

from transpiler.project.analyze import analyze_project


path = Path("sklearn/tree")

print(path)

graph = analyze_project(path)

print()
print("PROJECT SUMMARY")
print("=" * 80)

print(
    f"files:    {len(graph.files)}"
)

print(
    f"imports:  "
    f"{sum(len(i) for i in graph.imports.values())}"
)

print()

print("IMPORTS")
print("=" * 80)

import_count = 0

for file_path, imports in sorted(graph.imports.items()):

    if not imports:
        continue

    print()
    print(file_path)

    for imp in imports:

        print(vars(imp))

print()
print(
    f"Total imports: {import_count}"
)