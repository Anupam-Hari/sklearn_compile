import ast
from pathlib import Path

from transpiler_custom.parser.python_parser import parse_python_file as parse_file

tree = parse_file(Path("sklearn/__init__.py"))

for node in ast.walk(tree):

    if isinstance(node, ast.Assign):

        print(ast.dump(node))