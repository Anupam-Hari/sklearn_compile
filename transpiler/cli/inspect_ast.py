from pathlib import Path
import ast

from transpiler.parser.python_parser import parse_python_file


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE = (
    PROJECT_ROOT
    / "sklearn"
    / "sklearn"
    / "tree"
    / "_classes.py"
)


def walk(node, depth=0):
    print(" " * depth + type(node).__name__)

    for child in ast.iter_child_nodes(node):
        walk(child, depth + 2)


def main():
    tree = parse_python_file(SOURCE)

    walk(tree)


if __name__ == "__main__":
    main()