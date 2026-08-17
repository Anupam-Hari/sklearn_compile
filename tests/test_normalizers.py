from pathlib import Path
from pprint import pprint

from transpiler.normalizer.cython_normalizer import (
    normalize_cython_ast,
)
from transpiler.normalizer.python_normalizer import (
    normalize_python_ast,
)
from transpiler.parser.cython_parser import (
    parse_cython_file,
)
from transpiler.parser.python_parser import (
    parse_python_file,
)


PYTHON_FILE = Path(
    "sklearn/tree/_classes.py",
)

CYTHON_FILE = Path(
    "sklearn/tree/_splitter.pyx",
)

# print(PYTHON_FILE)
# print(PYTHON_FILE.resolve())
# print(PYTHON_FILE.exists())
# print(PYTHON_FILE.is_dir())

# print(CYTHON_FILE)
# print(CYTHON_FILE.resolve())
# print(CYTHON_FILE.exists())
# print(CYTHON_FILE.is_dir())


def print_node(node, indent=0):

    prefix = "    " * indent

    print(
        f"{prefix}"
        f"{node.node_type}: "
        f"{node.name}"
    )

    if hasattr(node, "bases") and node.bases:

        print(
            f"{prefix}    bases: "
            f"{node.bases}"
        )

    if hasattr(node, "module"):

        print(
            f"{prefix}    module: "
            f"{node.module}"
        )

    if hasattr(node, "names"):

        print(
            f"{prefix}    names: "
            f"{node.names}"
        )

    for child in node.children:

        print_node(
            child,
            indent + 1,
        )


def test_python():

    print()
    print("=" * 80)
    print("PYTHON")
    print("=" * 80)

    tree = parse_python_file(
        PYTHON_FILE,
    )

    module = normalize_python_ast(
        tree,
    )

    print()
    print("IMPORTS")
    print("-" * 40)

    pprint(module.imports)

    print()
    print("CLASSES")
    print("-" * 40)

    pprint(module.classes)

    print()
    print("FUNCTIONS")
    print("-" * 40)

    pprint(module.functions)

    print()
    print("NORMALIZED TREE")
    print("-" * 40)

    print_node(
        module,
    )


def test_cython():

    print()
    print("=" * 80)
    print("CYTHON")
    print("=" * 80)

    tree = parse_cython_file(
        CYTHON_FILE,
    )

    module = normalize_cython_ast(
        tree,
    )

    print()
    print("IMPORTS")
    print("-" * 40)

    pprint(module.imports)

    print()
    print("CLASSES")
    print("-" * 40)

    pprint(module.classes)

    print()
    print("FUNCTIONS")
    print("-" * 40)

    pprint(module.functions)

    print()
    print("NORMALIZED TREE")
    print("-" * 40)

    print_node(
        module,
    )


if __name__ == "__main__":

    # test_python()

    test_cython()