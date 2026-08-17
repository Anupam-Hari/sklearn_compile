import ast
from collections import Counter, defaultdict
from pathlib import Path

from Cython.Compiler.TreeFragment import (
    StringParseContext,
    parse_from_strings,
)

ROOT = Path("sklearn")

EXTENSIONS = {
    ".py",
    ".pyx",
    ".pxd",
    ".pxi",
}

cython_nodes = Counter()
python_nodes = Counter()

cython_examples = {}
python_examples = {}

cython_files = defaultdict(set)
python_files = defaultdict(set)

failed = []


def walk_python(node):

    nodes = []

    for child in ast.walk(node):

        nodes.append(child)

    return nodes


def walk_cython(node, nodes, visited):

    if node is None:
        return

    if not hasattr(node, "__dict__"):
        return

    node_id = id(node)

    if node_id in visited:
        return

    visited.add(node_id)

    nodes.append(node)

    for value in vars(node).values():

        if hasattr(value, "__dict__"):

            walk_cython(
                value,
                nodes,
                visited,
            )

        elif isinstance(value, (list, tuple)):

            for item in value:

                if hasattr(item, "__dict__"):

                    walk_cython(
                        item,
                        nodes,
                        visited,
                    )


files = []

for path in ROOT.rglob("*"):

    if path.suffix in EXTENSIONS:

        files.append(path)

print(f"Found {len(files)} files")

for path in sorted(files):

    print(f"Parsing {path}")

    try:

        source = path.read_text(
            encoding="utf-8",
        )

    except Exception as e:

        failed.append(
            (path, str(e))
        )

        continue

    try:

        if path.suffix == ".py":

            tree = ast.parse(
                source,
            )

            for node in walk_python(tree):

                node_type = type(node).__name__

                python_nodes[node_type] += 1

                python_files[node_type].add(
                    str(path),
                )

                if node_type not in python_examples:

                    example = {}

                    if hasattr(node, "name"):

                        example["name"] = node.name

                    python_examples[node_type] = example

        else:

            context = StringParseContext(
                str(path),
            )

            tree = parse_from_strings(
                name=str(path),
                code=source,
                context=context,
            )

            nodes = []

            walk_cython(
                tree,
                nodes,
                set(),
            )

            for node in nodes:

                node_type = type(node).__name__

                cython_nodes[node_type] += 1

                cython_files[node_type].add(
                    str(path),
                )

                if node_type not in cython_examples:

                    example = {}

                    for attr in (
                        "name",
                        "class_name",
                        "func_name",
                        "cname",
                    ):

                        value = getattr(
                            node,
                            attr,
                            None,
                        )

                        if value is not None:

                            example[attr] = value

                    cython_examples[node_type] = example

    except Exception as e:

        failed.append(
            (path, str(e))
        )


print()
print("=" * 80)
print("PYTHON NODES")
print("=" * 80)

for name, count in python_nodes.most_common():

    print(
        f"{name:<40}"
        f"{count:>8}"
    )


print()
print("=" * 80)
print("CYTHON NODES")
print("=" * 80)

for name, count in cython_nodes.most_common():

    print(
        f"{name:<40}"
        f"{count:>8}"
    )


print()
print("=" * 80)
print("CYTHON NODE EXAMPLES")
print("=" * 80)

for name in sorted(cython_examples):

    print()
    print(name)

    for key, value in cython_examples[name].items():

        print(
            f"    {key} = {value}"
        )

    print(
        f"    files = "
        f"{len(cython_files[name])}"
    )


print()
print("=" * 80)
print("FAILED FILES")
print("=" * 80)

for path, error in failed:

    print(path)
    print(f"    {error}")