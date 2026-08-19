from pathlib import Path

from transpiler_custom.parser.python_parser import parse_python_file
from transpiler_custom.parser.cython_pyx_parser import parse_cython_pyx
from transpiler_custom.parser.cython_pxd_parser import parse_cython_pxd
from transpiler_custom.normalizer.normalize_imports import normalize_imports
from transpiler_custom.resolver.import_resolver import resolve_import


TEST_FILES = [
    Path("sklearn/ensemble/_forest.py"),
    Path("sklearn/tree/_tree.pyx"),
    Path("sklearn/tree/_tree.pxd"),
]


for path in TEST_FILES:

    print(f"\n=== {path} ===\n")

    if path.suffix == ".py":
    
        tree = parse_python_file(path)

    elif path.suffix == ".pyx":

        tree = parse_cython_pyx(path)

    elif path.suffix == ".pxd":

        tree = parse_cython_pxd(path)

    else:

        continue

    imports = normalize_imports(
            tree=tree,
            source_file=path,
        )
    
    for import_node in imports:

        resolved = resolve_import(import_node)

        print(resolved)