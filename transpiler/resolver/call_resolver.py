from transpiler.dependency.models import (
    DependencyGraph,
    Symbol,
)

from transpiler.dependency.calls import (
    extract_calls,
)

from transpiler.resolver.import_resolver import (
    resolve_import_symbol,
)


def build_function_index(
    graph: DependencyGraph,
) -> dict[str, list[Symbol]]:

    functions = {}

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if symbol.symbol_type != "function":

                continue

            functions.setdefault(
                symbol.name,
                [],
            ).append(symbol)

    return functions


def resolve_call(
    graph: DependencyGraph,
    call_name: str,
) -> Symbol | None:

    if "." in call_name:

        return None

    matches = graph.function_index.get(
        call_name,
        [],
    )

    if not matches:

        return None

    return matches[0]


def find_method_in_class(
    graph: DependencyGraph,
    class_name: str,
    method_name: str,
) -> Symbol | None:

    class_symbol = graph.class_index.get(
        class_name,
    )

    # print(class_symbol)

    if class_symbol is None:

        return None

    for symbol in graph.symbols.get(
        class_symbol.file_path,
        [],
    ):

        if (
            symbol.parent == class_name
            and symbol.symbol_type == "function"
            and symbol.name == method_name
        ):

            return symbol

    return None


def resolve_imported_call(
    graph,
    file_path,
    call_name,
):

    for imported in graph.imports.get(
        file_path,
        [],
    ):

        if imported.name != call_name:

            continue

        return resolve_import_symbol(
            graph,
            imported,
        )

    return None

def resolve_self_call(
    graph: DependencyGraph,
    class_name: str,
    call_name: str,
) -> Symbol | None:

    if not call_name.startswith(
        "self."
    ):

        return None

    method_name = (
        call_name
        .split(".", 1)[1]
        .split("(", 1)[0]
    )

    return find_method_in_class(
        graph,
        class_name,
        method_name,
    )

def resolve_super_call(
    graph,
    class_name,
    call_name,
):

    if not call_name.startswith(
        "super()."
    ):

        return None

    class_symbol = graph.class_index.get(
        class_name,
    )

    if class_symbol is None:

        return None

    if not class_symbol.base_classes:

        return None

    method_name = (
        call_name
        .split(".", 1)[1]
        .split("(", 1)[0]
    )

    # print(
    #     class_name,
    #     class_symbol.base_classes,
    #     method_name,
    # )

    for base_class in (
        class_symbol.base_classes
    ):

        parent_method = (
            find_method_in_class(
                graph,
                base_class,
                method_name,
            )
        )

        # print(
        #     class_name,
        #     "->",
        #     base_class,
        #     "->",
        #     method_name,
        #     "->",
        #     parent_method,
        # )

        if parent_method is not None:

            return parent_method

    return None

def resolve_calls(
    graph: DependencyGraph,
) -> None:

    graph.function_index = (
        build_function_index(
            graph,
        )
    )

    graph.resolved_calls = {}

    for file_path, calls in graph.calls.items():

        resolved = []

        for call in calls:

            symbol = None

            if (
                call.name.startswith(
                    "self."
                )
                and call.parent_class
            ):

                symbol = resolve_self_call(
                    graph,
                    call.parent_class,
                    call.name,
                )

            elif (
                call.name.startswith(
                    "super()."
                )
                and call.parent_class
            ):

                symbol = resolve_super_call(
                    graph,
                    call.parent_class,
                    call.name,
                )

            elif "." not in call.name:

                symbol = resolve_call(
                    graph,
                    call.name,
                )

                if symbol is None:

                    symbol = resolve_imported_call(
                        graph,
                        file_path,
                        call.name,
                    )

            else:

                symbol = resolve_call(
                    graph,
                    call.name,
                )

            if symbol is not None:

                resolved.append(
                    symbol,
                )

        graph.resolved_calls[
            file_path
        ] = resolved