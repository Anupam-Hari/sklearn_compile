from pathlib import Path

from transpiler.cython.method_extractor import (
    extract_method,
)

from transpiler.cython.block_parser import (
    parse_blocks,
)

from transpiler.cython.ir_builder import (
    build_ir,
)


path = Path(
    "sklearn/sklearn/tree/_tree.pyx"
)

method = extract_method(
    path,
    "DepthFirstTreeBuilder",
    "build",
)

tree = parse_blocks(
    method
)

graph = build_ir(
    tree
)

for i, op in enumerate(
    graph.operations
):

    print(i, op)