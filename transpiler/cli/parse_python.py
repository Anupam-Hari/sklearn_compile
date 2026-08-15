from pathlib import Path

from transpiler.parser.python_parser import parse_python_file


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE = (
    PROJECT_ROOT
    / "sklearn"
    / "sklearn"
    / "tree"
    / "_classes.py"
)


def main():
    tree = parse_python_file(SOURCE)

    print(type(tree))


if __name__ == "__main__":
    main()