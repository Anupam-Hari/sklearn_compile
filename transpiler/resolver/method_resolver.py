def find_class_methods(
    graph,
    class_name,
):

    methods = []

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if (
                symbol.symbol_type == "function"
                and symbol.parent == class_name
            ):

                methods.append(
                    symbol,
                )

    return methods

def find_class_symbol(
    graph,
    class_name,
):

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if (
                symbol.symbol_type == "class"
                and symbol.name == class_name
            ):

                return symbol

    return None

def resolve_methods(
    graph,
    class_name,
    visited=None,
):

    if visited is None:

        visited = set()

    if class_name in visited:

        return []

    visited.add(
        class_name,
    )

    methods = []

    methods.extend(

        find_class_methods(
            graph,
            class_name,
        )
    )

    class_symbol = find_class_symbol(
        graph,
        class_name,
    )

    if class_symbol is None:

        return methods

    for base_class in (
        class_symbol.base_classes
        or []
    ):

        methods.extend(

            resolve_methods(

                graph,

                base_class,

                visited,
            )
        )

    return methods