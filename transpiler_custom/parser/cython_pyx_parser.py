from pathlib import Path

from Cython.Compiler import Errors, Options
from Cython.Compiler.Main import (
    CompilationOptions,
    Context,
    default_options,
)
from Cython.Compiler.Scanning import FileSourceDescriptor
from transpiler_custom.parser.utils import path_to_module

SKLEARN_ROOT = Path("sklearn").resolve()

def parse_cython_pyx(path: str | Path):

    path = Path(path).resolve()

    module_name = path_to_module(path, SKLEARN_ROOT)

    options = CompilationOptions(default_options)

    Errors.init_thread()

    context = Context(
        include_directories=[str(SKLEARN_ROOT)],
        compiler_directives=options.compiler_directives,
        options=options,
    )

    source_desc = FileSourceDescriptor(str(path))

    initial_pos = (source_desc, 1, 0)

    saved = Options.cimport_from_pyx

    Options.cimport_from_pyx = False

    scope = context.find_module(
        module_name,
        pos=initial_pos,
        need_pxd=0,
    )

    Options.cimport_from_pyx = saved

    return context.parse(
        source_desc=source_desc,
        scope=scope,
        pxd=False,
        full_module_name=module_name,
    )