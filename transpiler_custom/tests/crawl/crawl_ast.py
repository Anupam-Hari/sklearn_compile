from collections import Counter
from pathlib import Path
import ast

from transpiler_custom.parser.parser import parse_file


python_nodes = Counter()
cython_nodes = Counter()


def walk(node, counter):

    if node is None:

        return

    node_type = type(node).__name__

    counter[node_type] += 1

    if isinstance(node, ast.AST):

        for child in ast.iter_child_nodes(node):

            walk(child, counter)

        return

    for child_attr in getattr(node, "child_attrs", ()):

        value = getattr(node, child_attr, None)

        if isinstance(value, list):

            for item in value:

                if hasattr(item, "child_attrs"):

                    walk(item, counter)

        elif hasattr(value, "child_attrs"):

            walk(value, counter)


for path in Path("sklearn").rglob("*"):

    if path.suffix not in {".py", ".pyx", ".pxd"}:

        continue

    try:

        tree = parse_file(path)

    except Exception as e:

        print(f"FAILED: {path}")
        print(type(e).__name__)
        print(e)

        continue

    if path.suffix == ".py":

        walk(tree, python_nodes)

    else:

        walk(tree, cython_nodes)


print("\n=== PYTHON NODES ===\n")

for node_type, count in sorted(python_nodes.items()):

    print(f"{node_type}: {count}")


print("\n=== CYTHON NODES ===\n")

for node_type, count in sorted(cython_nodes.items()):

    print(f"{node_type}: {count}")