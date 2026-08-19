from pathlib import Path

from transpiler_custom.models.symbols import (
    ResolvedSymbolNode,
    SymbolNode,
)


def resolve_symbol(
    symbol_node: SymbolNode,
) -> ResolvedSymbolNode:

    return ResolvedSymbolNode(
        original=symbol_node,
        resolved_file=Path(
            symbol_node.source_file
        ),
        external=False,
    )