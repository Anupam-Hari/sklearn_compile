from pathlib import Path

from transpiler.parser.python_parser import parse_python_file
from transpiler.normalizer.python_normalizer import (
    normalize_python_ast,
)


def walk(node, depth=0):

    if node.node_type == "call":

        print(
            "CALL:",
            repr(node.name),
        )

    for child in node.children:

        walk(
            child,
            depth + 1,
        )


tree = parse_python_file(
    Path(
        "sklearn/tree/_classes.py",
    )
)

module = normalize_python_ast(
    tree,
)

walk(
    module,
)