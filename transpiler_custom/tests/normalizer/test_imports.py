from pathlib import Path

from transpiler_custom.parser.parser import parse_file
from transpiler_custom.normalizer.normalize_imports import normalize_imports


FILES = [
    Path("sklearn/ensemble/_forest.py"),
    Path("sklearn/tree/_tree.pyx"),
    Path("sklearn/tree/_tree.pxd"),
]


for path in FILES:

    print(f"\n=== {path} ===\n")

    tree = parse_file(path)

    imports = normalize_imports(
        tree=tree,
        source_file=path,
    )

    for import_node in imports:

        print(import_node)