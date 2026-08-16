from pathlib import Path

from transpiler.cython.method_extractor import (
    extract_method,
)

from transpiler.cython.block_parser import (
    parse_blocks,
)


def print_tree(node, depth=0):

    prefix = "    " * depth

    print(
        prefix,
        type(node).__name__,
        getattr(node, "kind", ""),
        getattr(node, "condition", ""),
        getattr(node, "name", ""),
        getattr(node, "target", ""),
        getattr(node, "value", ""),
    )

    for child in getattr(
        node,
        "children",
        [],
    ):

        print_tree(
            child,
            depth + 1,
        )


method = extract_method(
    Path(
        "sklearn/sklearn/tree/_tree.pyx"
    ),
    "DepthFirstTreeBuilder",
    "build",
)

tree = parse_blocks(
    method
)

print_tree(
    tree
)