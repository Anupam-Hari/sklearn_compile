from transpiler.dependency.models import (
    DependencyGraph,
    Symbol,
)


def build_class_index(
    graph: DependencyGraph,
) -> dict[str, Symbol]:

    classes = {}

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if symbol.symbol_type != "class":

                continue

            classes[symbol.name] = symbol

    return classes


def resolve_base_classes(
    graph: DependencyGraph,
    class_symbol: Symbol,
) -> list[Symbol]:

    if not class_symbol.base_classes:

        return []

    parents = []

    for base_class in class_symbol.base_classes:

        parent = graph.class_index.get(
            base_class,
        )

        if parent is not None:

            parents.append(
                parent,
            )

    return parents


def resolve_classes(
    graph: DependencyGraph,
) -> None:

    graph.class_index = (
        build_class_index(
            graph,
        )
    )

    graph.class_inheritance = {}

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if symbol.symbol_type != "class":

                continue

            parents = resolve_base_classes(
                graph,
                symbol,
            )

            graph.class_inheritance[
                symbol.name
            ] = parents