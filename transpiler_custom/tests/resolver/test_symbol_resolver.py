from pathlib import Path

from transpiler_custom.normalizer.normalize_symbols import (
    normalize_symbols,
)
from transpiler_custom.parser.parser import parse_file


TEST_FILES = [
    Path("sklearn/ensemble/_forest.py"),
    Path("sklearn/tree/_tree.pyx"),
    Path("sklearn/tree/_tree.pxd"),
]


for path in TEST_FILES:

    print(f"\n=== {path} ===\n")

    tree = parse_file(path)

    symbols = normalize_symbols(
        tree=tree,
        source_file=path,
    )

    for symbol in symbols:

        print(
            f"{symbol.kind:<20}"
            f"{symbol.name:<40}"
            f"{str(symbol.source_file):<35}"
            f"{str(symbol.parent_name):<30}"
            f"{str(symbol.parent_kind)}"
        )