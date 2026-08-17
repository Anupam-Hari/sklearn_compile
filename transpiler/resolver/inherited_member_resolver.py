from transpiler.dependency.models import Symbol

def find_class(
    graph,
    class_name,
):

    if not hasattr(
        graph,
        "class_index",
    ):

        return None

    return graph.class_index.get(
        class_name,
    )


def get_inherited_methods(
    graph,
    class_symbol,
    visited=None,
):

    if visited is None:

        visited = set()

    if class_symbol.name in visited:

        return []

    visited.add(
        class_symbol.name,
    )

    methods = []

    local_method_names = set()

    for symbol in graph.symbols.get(
        class_symbol.file_path,
        [],
    ):

        if (
            symbol.parent == class_symbol.name
            and symbol.symbol_type == "function"
        ):

            if symbol.inherited_from is None:

                methods.append(
                    symbol,
                )
                local_method_names.add(
                    symbol.name,
                )

    if not class_symbol.base_classes:

        return methods

    for base_class in (
        class_symbol.base_classes
    ):

        parent = find_class(
            graph,
            base_class,
        )

        if parent is None:

            continue

        parent_methods = get_inherited_methods(
            graph,
            parent,
            visited,
        )

        for method in parent_methods:

            if method.name in local_method_names:
                continue

            inherited_method = Symbol(
                name=method.name,
                symbol_type=method.symbol_type,
                file_path=method.file_path,
                language=method.language,
                parent=class_symbol.name,
                inherited_from=parent.name,
            )

            methods.append(
                inherited_method,
            )

    return methods


def resolve_inherited_members(
    graph,
):

    inherited_members = {}

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if (
                symbol.symbol_type
                != "class"
            ):

                continue

            members = get_inherited_methods(
                graph,
                symbol,
            )

            inherited_members[
                symbol.name
            ] = members

    return inherited_members