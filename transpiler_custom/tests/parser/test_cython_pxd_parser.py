from pathlib import Path

from parser.cython_pxd_parser import parse_cython_pxd


seen = set()


def walk(node):

    node_type = type(node).__name__

    if node_type not in seen:

        seen.add(node_type)

        print(f"\n{node_type}")
        print(node.__dict__.keys())

        print(node.__dict__)

    for child_attr in getattr(node, "child_attrs", ()):

        value = getattr(node, child_attr, None)

        if isinstance(value, list):

            for item in value:

                if hasattr(item, "child_attrs"):

                    walk(item)

        elif hasattr(value, "child_attrs"):

            walk(value)


tree = parse_cython_pxd(
    Path(
        "/home/anupam/Anupam/sklearn_compile/sklearn/tree/_tree.pxd"
    )
)

walk(tree)