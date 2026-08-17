def build_function_index(graph):

    functions = {}

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if symbol.symbol_type != "function":

                continue

            functions.setdefault(
                symbol.name,
                [],
            ).append(
                symbol,
            )

    return functions

def resolve_call(
    graph,
    call_name,
):

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
    graph,
    class_name,
    method_name,
):

    class_symbol = graph.class_index.get(
        class_name,
    )

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

def resolve_self_call(
    graph,
    class_name,
    call_name,
):

    if not call_name.startswith(
        "self."
    ):

        return None

    method_name = call_name.split(
        ".",
        1,
    )[1]

    return find_method_in_class(
        graph,
        class_name,
        method_name,
    )