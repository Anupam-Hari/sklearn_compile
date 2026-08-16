from pathlib import Path

from Cython.Compiler.Main import Context
from Cython.Compiler.Main import CompilationOptions
from Cython.Compiler.TreeFragment import parse_from_strings


def parse_cython_file(path: str | Path):

    path = Path(path)

    source = path.read_text()

    context = Context.from_options(
        CompilationOptions()
    )

    tree = parse_from_strings(
        name=str(path),
        code=source,
        context=context,
    )

    return tree