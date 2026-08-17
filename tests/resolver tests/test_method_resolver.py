from pathlib import Path

from transpiler.project.analyze import (
    analyze_project,
)

from transpiler.resolver.method_resolver import (
    resolve_methods,
)

graph = analyze_project(
    Path("sklearn/tree"),
)

for class_symbols in graph.symbols.values():

    for symbol in class_symbols:

        if symbol.symbol_type != "class":

            continue

        print()
        print(symbol.name)

        methods = resolve_methods(
            graph,
            symbol.name,
        )

        seen = set()

        for method in methods:

            if method.name in seen:

                continue

            seen.add(
                method.name,
            )

            print(
                f"    {method.name}"
            )