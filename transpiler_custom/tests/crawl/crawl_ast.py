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


def print_attribute(
    name,
    value,
    indent=0,
    visited=None,
):

    if visited is None:

        visited = set()

    prefix = "    " * indent

    print(
        f"{prefix}{name}: "
        f"({type(value).__name__})"
    )

    if value is None:

        print(
            f"{prefix}    None"
        )

        return

    if isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
            bytes,
        ),
    ):

        print(
            f"{prefix}    {repr(value)}"
        )

        return

    if isinstance(
        value,
        tuple,
    ):

        print(
            f"{prefix}    {repr(value)}"
        )

        return

    if isinstance(
        value,
        list,
    ):

        print(
            f"{prefix}    list[{len(value)}]"
        )

        for i, item in enumerate(value):

            print_attribute(
                f"[{i}]",
                item,
                indent + 1,
                visited,
            )

        return

    if not hasattr(
        value,
        "__dict__",
    ):

        print(
            f"{prefix}    {repr(value)}"
        )

        return

    object_id = id(value)

    if object_id in visited:

        return

    visited.add(object_id)

    for key, child in sorted(
        value.__dict__.items()
    ):

        print_attribute(
            key,
            child,
            indent + 1,
            visited,
        )

def print_node_details(node):

    node_type = type(node).__name__

    if node_type in printed_nodes:

        return

    printed_nodes.add(node_type)

    print(
        "\n"
        + "=" * 80
    )

    print(node_type)

    print(
        "=" * 80
    )

    visited = {
        id(node),
    }

    for key, value in sorted(
        node.__dict__.items()
    ):

        print_attribute(
            key,
            value,
            visited=visited,
        )

    print()

    print("child_attrs:")

    print(
        getattr(
            node,
            "child_attrs",
            (),
        )
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