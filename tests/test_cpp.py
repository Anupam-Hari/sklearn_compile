from pathlib import Path

from transpiler.parser.python_parser import parse_python_file
from transpiler.normalizer.python_normalizer import (
    normalize_python_ast,
)

path = Path("examples/input.py")

tree = parse_python_file(path)

module = normalize_python_ast(tree)

print(module)