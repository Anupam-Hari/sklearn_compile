from transpiler.cython.calls import (
    extract_calls,
)
from transpiler.cython.method_resolver import (
    resolve_cython_method,
)
from transpiler.cython.variable_types import (
    extract_variable_types,
)


def walk_cython(
    graph,
    class_name,
    method_name,
    depth=0,
    visited=None,
):

    if visited is None:
        visited = set()

    key = (
        class_name,
        method_name,
    )

    if key in visited:
        return

    visited.add(key)

    print(
        "    " * depth
        + f"{class_name}.{method_name}"
    )

    source = resolve_cython_method(
        graph,
        class_name,
        method_name,
    )

    if not source:
        return

    symbol = graph

    method_symbol = next(
        s
        for symbols in graph.symbols.values()
        for s in symbols
        if s.name == class_name
    )

    variables = extract_variable_types(
        method_symbol.file_path
    )

    for dependency in extract_calls(source):

        print(
            "    " * (depth + 1)
            + dependency
        )

        if "." not in dependency:
            continue

        obj, called_method = dependency.split(
            ".",
            1,
        )

        if obj not in variables:
            continue

        walk_cython(
            graph,
            variables[obj],
            called_method,
            depth + 2,
            visited,
        )