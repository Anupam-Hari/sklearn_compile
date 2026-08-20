# parser/cython_pxd_parser.py

from pathlib import Path

from Cython.Compiler import Errors
from Cython.Compiler.Main import (
    CompilationOptions,
    Context,
    default_options,
)
from Cython.Compiler.Scanning import FileSourceDescriptor


def parse_cython_pxd(path: str | Path):

    path = Path(path).resolve()

    Errors.init_thread()

    options = CompilationOptions(default_options)

    context = Context(
        include_directories=[
            str(path.parent.parent.parent),
        ],
        compiler_directives=options.compiler_directives,
        options=options,
    )

    scope = context.find_module(
        path.with_suffix("").relative_to(path.parent.parent.parent)
        .as_posix()
        .replace("/", "."),
        need_pxd=0,
    )

    return context.parse(
        source_desc=FileSourceDescriptor(str(path)),
        scope=scope,
        pxd=True,
        full_module_name=path.with_suffix("")
        .relative_to(path.parent.parent.parent)
        .as_posix()
        .replace("/", "."),
    )