import ast
from pathlib import Path


def parse_python_file(path: str | Path) -> ast.Module:
    path = Path(path)

    with open(path, "r") as f:
        source = f.read()

    return ast.parse(source)