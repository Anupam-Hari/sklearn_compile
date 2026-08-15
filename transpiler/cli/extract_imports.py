from pathlib import Path

from transpiler.dependency.imports import extract_imports
from transpiler.normalizer.python_normalizer import normalize_python_ast
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

    module = normalize_python_ast(tree)

    imports = extract_imports(module)

    for imp in imports:
        print(imp)


if __name__ == "__main__":
    main()