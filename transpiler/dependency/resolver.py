from pathlib import Path

from transpiler.dependency.models import DependencyGraph
from transpiler.dependency.models import Symbol


def find_symbol(
    graph: DependencyGraph,
    name: str,
) -> Symbol | None:

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if symbol.name == name:
                return symbol

    return None


def find_symbols_in_file(
    graph: DependencyGraph,
    file_path: Path,
) -> list[Symbol]:

    return graph.symbols.get(file_path, [])