from pathlib import Path

from transpiler.project.analyze import analyze_project


path = Path("sklearn/tree")

print(path)
# print(path.resolve())
# print(path.exists())
# print(path.is_dir())

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

print(
    f"symbols:  "
    f"{sum(len(s) for s in graph.symbols.values())}"
)

print()
print("SYMBOL TYPES")
print("=" * 80)

symbol_counts = {}
count = 0

for symbols in graph.symbols.values():

    for symbol in symbols:

        # if symbol.symbol_type == "variable":

        #     print(symbol)

        #     count += 1

        #     if count == 50:

        #         break

        symbol_type = symbol.symbol_type

        symbol_counts[symbol_type] = (
            symbol_counts.get(
                symbol_type,
                0,
            )
            + 1
        )
    # if count == 50:
    #         break

for symbol_type, count in sorted(
    symbol_counts.items()
):

    print(
        f"{symbol_type:<12}"
        f"{count}"
    )