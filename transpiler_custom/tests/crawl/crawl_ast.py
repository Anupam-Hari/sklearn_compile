from collections import Counter
from pathlib import Path
import ast

from transpiler_custom.parser.parser import parse_file


python_nodes = Counter()
cython_nodes = Counter()

printed_nodes = set()

SKIP_NODES = {
    "NameNode",
    "IdentifierStringNode",
    "IntNode",
    "FloatNode",
    "StringNode",
    "UnicodeNode",
    "BytesNode",
}


def print_node_details(node):

    node_type = type(node).__name__

    if node_type in printed_nodes:

        return

    printed_nodes.add(node_type)

    print("\n" + "=" * 80)
    print(node_type)
    print("=" * 80)

    for key, value in sorted(node.__dict__.items()):

        value_type = type(value).__name__

        if isinstance(value, list):

            print(
                f"{key}: "
                f"list[{len(value)}]"
            )

        else:

            print(
                f"{key}: "
                f"{value!r} "
                f"({value_type})"
            )


def walk(node, counter):

    if node is None:

        return

    node_type = type(node).__name__

    counter[node_type] += 1

    if node_type not in SKIP_NODES:

        print_node_details(node)

    if isinstance(node, ast.AST):

        for child in ast.iter_child_nodes(node):

            walk(
                child,
                counter,
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

                if (
                    item is not None
                    and hasattr(
                        item,
                        "child_attrs",
                    )
                ):

                    walk(
                        item,
                        counter,
                    )

        elif (
            value is not None
            and hasattr(
                value,
                "child_attrs",
            )
        ):

            walk(
                value,
                counter,
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
        continue

    if path.suffix == ".py":

        walk(
            tree,
            python_nodes,
        )

    else:

        walk(
            tree,
            cython_nodes,
        )

print("\n")
print("=" * 80)
print("PYTHON NODE COUNTS")
print("=" * 80)

for name, count in python_nodes.most_common():

    print(f"{name}: {count}")

print("\n")
print("=" * 80)
print("CYTHON NODE COUNTS")
print("=" * 80)

for name, count in cython_nodes.most_common():

    print(f"{name}: {count}")