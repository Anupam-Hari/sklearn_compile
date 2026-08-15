from pathlib import Path
import ast

from .models import ASTNode


def parse_python_file(path: Path) -> ast.Module:
    source = path.read_text(encoding="utf-8")

    return ast.parse(source, filename=str(path))