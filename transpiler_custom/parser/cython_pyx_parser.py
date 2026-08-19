from pathlib import Path

from Cython.Compiler.TreeFragment import StringParseContext, parse_from_strings

def parse_cython_pyx(path: str | Path):
    """Parse a .pyx or .pxd file and return Cython's native compiler AST."""

    path = Path(path).resolve()

    source = path.read_text(encoding="utf-8")

    context = StringParseContext(str(path))

    return parse_from_strings(
        name=str(path),
        code=source,
        context=context,
    )