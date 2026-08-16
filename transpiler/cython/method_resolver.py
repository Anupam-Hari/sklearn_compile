from pathlib import Path

from transpiler.cython.method_extractor import (
    extract_method,
)
from transpiler.dependency.resolver import (
    find_symbol,
)


def resolve_cython_method(
    graph,
    class_name: str,
    method_name: str,
):

    symbol = find_symbol(
        graph,
        class_name,
    )

    if symbol is None:
        return None

    return extract_method(
        symbol.file_path,
        class_name,
        method_name,
    )