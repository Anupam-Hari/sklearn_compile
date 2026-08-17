from pathlib import Path

from transpiler.project.analyze import (
    analyze_project,
)

from transpiler.resolver.class_resolver import (
    resolve_classes,
)

graph = analyze_project(
    Path("sklearn/tree"),
)

inheritance = resolve_classes(
    graph,
)

for symbols in graph.symbols.values():

    for symbol in symbols:

        if symbol.symbol_type == "class":

            print(
                symbol.name,
                "->",
                symbol.base_classes,
            )

print()

print("CLASS INHERITANCE")

print("=" * 80)

for child, parents in inheritance.items():

    if not parents:

        continue

    print(
        child,
        "->",
        [parent.name for parent in parents],
    )