from collections import Counter
from pathlib import Path

from transpiler.normalizer.cython_normalizer import (
    normalize_cython_ast, UNHANDLED_CYTHON_NODES
)
from transpiler.normalizer.python_normalizer import (
    normalize_python_ast, UNHANDLED_PYTHON_NODES
)
from transpiler.parser.cython_parser import (
    parse_cython_file, 
)
from transpiler.parser.python_parser import (
    parse_python_file,
)

ROOT = Path("sklearn/tree")

def walk(
    node,
    counter,
    parent=None,
):

    counter[
        (
            parent,
            node.node_type,
            node.name,
        )
    ] += 1

    current_parent = parent

    if node.node_type in {
        "class",
        "function",
    }:

        current_parent = node.name

    for child in node.children:

        walk(
            child,
            counter,
            current_parent,
        )


def update_counts(module, counts):

    counts["imports"] += len(module.imports)
    counts["classes"] += len(module.classes)
    counts["functions"] += len(module.functions)
    counts["variables"] += len(module.variables)
    counts["constants"] += len(module.constants)
    counts["typedefs"] += len(module.typedefs)
    counts["structs"] += len(module.structs)
    counts["enums"] += len(module.enums)
    counts["total"] += len(module.children)


def print_summary(title, counts):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)

    for key, value in counts.items():

        print(f"{key:<12}{value}")


def test_python():

    counts = Counter()
    counter = Counter()

    python_files = sorted(ROOT.rglob("*.py"))

    for path in python_files:

        if "tests" in path.parts:
            continue

        print(f"Parsing {path}")

        try:

            tree = parse_python_file(path)

            module = normalize_python_ast(tree)

            counter = Counter()

            walk(
                module,
                counter,
            )

            duplicates = False

            for key, count in counter.items():

                if count > 1:

                    if not duplicates:

                        print()
                        print(f"DUPLICATES IN {path}")

                        duplicates = True

                    print(
                        key,
                        count,
                    )

            update_counts(
                module,
                counts,
            )

        except Exception as e:

            print(f"FAILED: {path}")
            print(e)

    print_summary(
        "PYTHON",
        counts,
    )


def test_cython():

    counts = Counter()

    cython_files = sorted(
        list(ROOT.rglob("*.pyx"))
        + list(ROOT.rglob("*.pxd"))
    )

    for path in cython_files:

        if "tests" in path.parts:
            continue

        print(f"Parsing {path}")

        try:

            tree = parse_cython_file(path)

            module = normalize_cython_ast(tree)

            update_counts(
                module,
                counts,
            )

        except Exception as e:

            print(f"FAILED: {path}")
            print(e)

    print_summary(
        "CYTHON",
        counts,
    )

    print()
    print("UNHANDLED PYTHON NODES")
    print("-" * 40)

    for node, count in UNHANDLED_PYTHON_NODES.items():

        print(f"{node:<30}{count}")

    print()
    print("UNHANDLED CYTHON NODES")
    print("-" * 40)

    for node, count in UNHANDLED_CYTHON_NODES.items():

        print(f"{node:<30}{count}")


if __name__ == "__main__":

    test_python()

    test_cython()