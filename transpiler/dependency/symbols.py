from transpiler.dependency.models import Symbol

def extract_symbols(
    module,
    file_path,
    language="python",
):

    symbols = []

    walk(
        module,
        symbols,
        file_path,
        language,
    )

    return symbols


def walk(
    node,
    symbols,
    file_path,
    language,
    parent=None,
):

    SYMBOL_TYPES = {
        "class": "class",
        "function": "function",
        "parameter": "parameter",
        "variable": "variable",
        "struct": "struct",
        "enum": "enum",
        "enum_value": "enum_value",
        "typedef": "typedef",
        "extern": "extern",
        "function_declarator": "function_declarator",
        "variable_declarator": "variable_declarator",
        "simple_type": "simple_type",
        "complex_type": "complex_type",
        "qualified_type": "qualified_type",
        "nested_type": "nested_type",
        "tuple_type": "tuple_type",
        "fused_type": "fused_type",
        "memory_view_type": "memory_view_type",
        "templated_type": "templated_type",
    }

    current_parent = parent

    if node.node_type in SYMBOL_TYPES:

        symbol_kwargs = {
            "name": node.name,
            "symbol_type": SYMBOL_TYPES[
                node.node_type
            ],
            "file_path": file_path,
            "language": language,
            "parent": parent,
        }

        if node.node_type == "class":

            symbol_kwargs[
                "base_classes"
            ] = getattr(
                node,
                "bases",
                [],
            )

            current_parent = node.name

        elif node.node_type == "function":

            current_parent = node.name

        symbols.append(
            Symbol(
                **symbol_kwargs,
            )
        )

    for child in getattr(
        node,
        "children",
        [],
    ):

        walk(
            child,
            symbols,
            file_path,
            language,
            current_parent,
        )
