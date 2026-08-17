from pathlib import Path

from transpiler.project.analyze import analyze_project


path = Path("sklearn")

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
print("RELATIVE IMPORTS")
print("=" * 80)

targets = {
    "_typing",
    "_internal",
    "_aliases",
}

for file_path, imports in sorted(graph.imports.items()):

    matches = [
        imp
        for imp in imports
        if imp.module in targets
    ]

    if not matches:
        continue

    print()
    print(file_path)

    for imp in matches:

        print(
            {
                "module": imp.module,
                "name": imp.name,
                "level": getattr(
                    imp,
                    "level",
                    None,
                ),
            }
        )