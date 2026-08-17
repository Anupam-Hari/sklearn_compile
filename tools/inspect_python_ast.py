import ast
from collections import Counter
from pathlib import Path


PATHS = [
    Path("sklearn/tree/_classes.py"),
    Path("sklearn/tree/_export.py"),
    Path("sklearn/tree/_reingold_tilford.py"),
    Path("sklearn/tree/__init__.py"),
]


node_counts = Counter()
node_examples = {}
file_counts = {}


for path in PATHS:

    source = path.read_text(encoding="utf-8")

    tree = ast.parse(
        source,
        filename=str(path),
    )

    current_file_counts = Counter()

    for node in ast.walk(tree):

        node_type = type(node).__name__

        node_counts[node_type] += 1
        current_file_counts[node_type] += 1

        if node_type not in node_examples:

            example = {}

            for attr in (
                "name",
                "id",
                "attr",
                "module",
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