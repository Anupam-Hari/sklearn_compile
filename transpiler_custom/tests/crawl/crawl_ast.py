from collections import Counter
from pathlib import Path
import ast

from transpiler_custom.parser.parser import parse_file


PYTHON_TARGETS = {
    # "Name",
    # "Attribute",
    # "Call",
}

CYTHON_TARGETS = {
    # "CTypeDefNode",
    # "CVarDefNode",
    "CFuncDefNode",
}


python_nodes = Counter()
cython_nodes = Counter()

printed_nodes = set()


def print_node_details(node):

    node_type = type(node).__name__

    if node_type in printed_nodes:

        return

    printed_nodes.add(node_type)

    print("\n" + "=" * 80)

    print(node_type)

    print()

    for key, value in sorted(node.__dict__.items()):

        print(f"{key}: {value}")

    print()


def walk(node, counter, targets):

    if node is None:

        return

    node_type = type(node).__name__

    counter[node_type] += 1

    if node_type in targets:

        print_node_details(node)
        print(node.declarator.base.__dict__)

    if isinstance(node, ast.AST):

        for child in ast.iter_child_nodes(node):

            walk(
                child,
                counter,
                targets,
            )

        return

    for child_attr in getattr(
        node,
        "child_attrs",
        (),
    ):

        value = getattr(
            node,
            child_attr,
            None,
        )

        if isinstance(value, list):

            for item in value:

                if hasattr(
                    item,
                    "child_attrs",
                ):

                    walk(
                        item,
                        counter,
                        targets,
                    )

        elif hasattr(
            value,
            "child_attrs",
        ):

            walk(
                value,
                counter,
                targets,
            )


for path in Path("sklearn").rglob("*"):

    if path.suffix not in {
        ".py",
        ".pyx",
        ".pxd",
    }:

        continue

    try:

        tree = parse_file(path)

    except Exception as e:

        print(f"FAILED: {path}")
        print(type(e).__name__)
        print(e)

        continue

    if path.suffix == ".py":

        walk(
            tree,
            python_nodes,
            PYTHON_TARGETS,
        )

    else:

        walk(
            tree,
            cython_nodes,
            CYTHON_TARGETS,
        )