import ast
from pathlib import Path


def parse_python_file(path: str | Path) -> ast.Module:

    path = Path(path)

    source = path.read_text()

    tree = ast.parse(
        source,
        filename=str(path),
    )

    return tree