from collections import Counter
from pathlib import Path
import ast

from parser.python_parser import parse_python_file
from parser.cython_pyx_parser import parse_cython_pyx
from parser.cython_pxd_parser import parse_cython_pxd


IMPORT_NODE_TYPES = {
    # Python
    "Import",
    "ImportFrom",

    # Cython
    "ImportNode",
    "CImportStatNode",
    "FromCImportStatNode",
}


seen = {}
counts = Counter()
pxi_files = []


def walk(node):

    node_type = type(node).__name__

    if node_type in IMPORT_NODE_TYPES:

        counts[node_type] += 1

        if node_type not in seen:

            seen[node_type] = node

    if isinstance(node, ast.AST):

        for child in ast.iter_child_nodes(node):

            walk(child)

        return

    for child_attr in getattr(node, "child_attrs", ()):

        value = getattr(node, child_attr, None)

        if isinstance(value, list):

            for item in value:

                if hasattr(item, "child_attrs"):

                    walk(item)

        elif hasattr(value, "child_attrs"):

            walk(value)


for path in Path("sklearn").rglob("*"):

    try:

        if path.suffix == ".py":

            tree = parse_python_file(path)

        elif path.suffix == ".pyx":

            tree = parse_cython_pyx(path)

        elif path.suffix == ".pxd":

            tree = parse_cython_pxd(path)

        elif path.suffix == ".pxi":

            pxi_files.append(path)

            continue

        else:

            continue

    except Exception as e:

        print(f"FAILED: {path}")
        print(type(e).__name__)
        print(e)

        continue

    walk(tree)


print("\n=== IMPORT NODE TYPES ===\n")

for node_type in sorted(seen):

    print(node_type)

    print(f"count: {counts[node_type]}")

    print(seen[node_type].__dict__.keys())

    print(seen[node_type].__dict__)

    print()


print("\n=== .pxi ===\n")

for path in sorted(pxi_files):

    print(path)