from pathlib import Path

from transpiler.project.analyze import analyze_project


graph = analyze_project(
    Path("sklearn/sklearn/tree")
)

print()

print("FILES")
print("=" * 40)

for path in sorted(graph.files):
    print(path)

print()

print("IMPORTS")
print("=" * 40)

for path, imports in graph.imports.items():

    if not imports:
        continue

    print()
    print(path)

    for symbol in imports:
        print(" ", symbol)

print()

print("SYMBOLS")
print("=" * 40)

for path, symbols in graph.symbols.items():

    if not symbols:
        continue

    print()
    print(path)

    for symbol in symbols:
        print(" ", symbol.name, symbol.symbol_type)