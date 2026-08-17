from pathlib import Path

from transpiler.project.analyze import analyze_project


path = Path("sklearn/tree")

print(path)
print(path.resolve())
print(path.exists())
print(path.is_dir())

graph = analyze_project(
    Path("sklearn/tree")
)

print()

print("FILES")
print("=" * 80)

for path in sorted(graph.files):
    print(path)

print()

print("IMPORTS")
print("=" * 80)

for path, imports in graph.imports.items():

    if not imports:
        continue

    print()
    print(path)

    for imp in imports:
        print(
            f"    {imp.module} -> {imp.name}"
        )

print()

print("SYMBOLS")
print("=" * 80)

for path, symbols in graph.symbols.items():

    if not symbols:
        continue

    print()
    print(path)

    for symbol in symbols:

        if symbol.parent:

            print(
                f"    {symbol.parent}.{symbol.name} ({symbol.symbol_type})"
            )

        else:

            print(
                f"    {symbol.name} ({symbol.symbol_type})"
            )