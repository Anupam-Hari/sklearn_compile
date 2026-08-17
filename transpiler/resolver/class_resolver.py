def build_class_index(graph):

    classes = {}

    for file_path, symbols in graph.symbols.items():

        for symbol in symbols:

            if symbol.symbol_type != "class":

                continue

            classes[symbol.name] = symbol

    return classes

def resolve_base_classes(
    graph,
    class_symbol,
):

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

def resolve_classes(graph):

    graph.class_index = build_class_index(
        graph,
    )

    inheritance = {}

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if symbol.symbol_type != "class":

                continue

            parent = resolve_base_classes(

                graph,

                symbol,
            )

            inheritance[symbol.name] = parent

    return inheritance

