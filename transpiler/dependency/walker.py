from pathlib import Path

from transpiler.project.analyze import analyze_project

from transpiler.dependency.resolver import find_symbol

from transpiler.dependency.filter import keep_dependency

from transpiler.dependency.type_normalizer import normalize_type

from transpiler.dependency.builtin_types import BUILTIN_TYPES

from transpiler.dependency.instantiations import (
    extract_instantiations,
)

from transpiler.dependency.method_calls import (
    extract_method_calls,
)

from transpiler.cython.method_extractor import (
    extract_method,
)

from transpiler.cython.calls import (
    extract_calls,
)

from transpiler.dependency.local_symbols import (
    extract_local_symbols,
)


def walk_method(
    root: Path,
    class_name: str,
    method_name: str,
    visited=None,
):

    if visited is None:
        visited = set()

    graph = analyze_project(root)

    _walk(
        graph,
        class_name,
        method_name,
        visited,
    )


def _walk(
    graph,
    class_name,
    method_name,
    visited,
):

    key = (class_name, method_name)

    if key in visited:
        return

    visited.add(key)

    symbol = find_symbol(
        graph,
        class_name,
    )

    if symbol is None:

        print(
            f"{class_name} not found"
        )

        return

    print()

    print(
        f"{class_name}.{method_name}"
    )

    if symbol.language == "python":

        walk_python(
            graph,
            symbol,
            method_name,
            visited,
        )

    elif symbol.language == "cython":

        walk_cython(
            graph,
            symbol,
            class_name,
            method_name,
            visited,
        )

def walk_python(
    graph,
    symbol,
    method_name,
    visited,
):

    instances = extract_instantiations(
        symbol.file_path
    )

    methods = extract_method_calls(
        symbol.file_path
    )

    for variable, called_method in methods.get(
        method_name,
        [],
    ):

        if not keep_dependency(
            variable,
            called_method,
        ):
            continue

        print(
            f"    {variable}.{called_method}"
        )

        if variable not in instances:
            continue

        for cls in instances[variable]:

            _walk(
                graph,
                cls,
                called_method,
                visited,
            )

def walk_cython(
    graph,
    symbol,
    class_name,
    method_name,
    visited,
):

    source = extract_method(
        symbol.file_path,
        class_name,
        method_name,
    )

    if source is None:
        return

    local_symbols = extract_local_symbols(
        source
    )

    calls = extract_calls(
        source
    )

    for call in calls:

        print(
            f"    {call}"
        )

        if "." not in call:
            continue

        variable, called_method = call.rsplit(
            ".",
            1,
        )

        if variable not in local_symbols:
            continue

        cls = local_symbols[
            variable
        ]

        cls = normalize_type(cls)

        if cls in BUILTIN_TYPES:
            continue

        _walk(
            graph,
            cls,
            called_method,
            visited,
        )