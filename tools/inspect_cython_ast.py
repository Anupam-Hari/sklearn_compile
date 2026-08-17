import ast
from collections import Counter
from pathlib import Path


PATHS = [
    Path("sklearn/tree/_criterion.pxd"),
    Path("sklearn/tree/_criterion.pyx"),
    Path("sklearn/tree/_partitioner.pxd"),
    Path("sklearn/tree/_partitioner.pyx"),
    Path("sklearn/tree/_splitter.pxd"),
    Path("sklearn/tree/_splitter.pyx"),
    Path("sklearn/tree/_tree.pxd"),
    Path("sklearn/tree/_tree.pyx"),
    Path("sklearn/tree/_utils.pxd"),
    Path("sklearn/tree/_utils.pyx"),
]


from Cython.Compiler.TreeFragment import (
    StringParseContext,
    parse_from_strings,
)


node_counts = Counter()
node_examples = {}
file_counts = {}


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


for path in PATHS:

    print(f"Parsing {path}")

    try:

        source = path.read_text(encoding="utf-8")

        context = StringParseContext(str(path))

        tree = parse_from_strings(
            name=str(path),
            code=source,
            context=context,
        )

    except Exception as e:

        print(f"FAILED: {path}")
        print(e)

        continue
    
    nodes = []

    walk_cython(
        tree,
        nodes,
        set(),
    )

    current_file_counts = Counter()

    for node in nodes:

        node_type = type(node).__name__

        node_counts[node_type] += 1
        current_file_counts[node_type] += 1

        if node_type not in node_examples:

            example = {}

            for attr in (
                "name",
                "class_name",
                "func_name",
                "cname",
            ):

                value = getattr(node, attr, None)

                if value is not None:

                    example[attr] = value

            node_examples[node_type] = example

    file_counts[str(path)] = current_file_counts


print()
print("FILES ANALYZED")
print("=" * 60)

for path in PATHS:

    print(path)

print()
print("=" * 60)
print("AGGREGATED NODE TYPES")
print("=" * 60)
print()

for name, count in node_counts.most_common():

    print(f"{name:<35}{count}")

print()
print("=" * 60)
print("NODE EXAMPLES")
print("=" * 60)

for name, example in node_examples.items():

    print()
    print(name)

    for key, value in example.items():

        print(f"    {key} = {value}")