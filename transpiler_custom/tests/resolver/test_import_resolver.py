from pathlib import Path

from transpiler_custom.parser.parser import parse_file
from transpiler_custom.normalizer.normalize_imports import normalize_imports
from transpiler_custom.resolver.import_resolver import resolve_import


TEST_FILES = [
    Path("sklearn/ensemble/_forest.py"),
    Path("sklearn/tree/_tree.pyx"),
    Path("sklearn/tree/_tree.pxd"),
]


for path in TEST_FILES:

    print(f"\n=== {path} ===\n")

    tree = parse_file(path)

    imports = normalize_imports(
            tree=tree,
            source_file=path,
        )
    
    for import_node in imports:

        resolved = resolve_import(import_node)

        print(resolved)