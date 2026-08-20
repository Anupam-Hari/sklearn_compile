from pathlib import Path

from transpiler_custom.parser.cython_pxd_parser import parse_cython_pxd
from transpiler_custom.parser.cython_pyx_parser import parse_cython_pyx
from transpiler_custom.parser.python_parser import parse_python_file


def parse_file(path: str | Path):

    path = Path(path)

    try:

        if path.suffix == ".py":

            return parse_python_file(path)

        elif path.suffix == ".pyx":

            return parse_cython_pyx(path)

        elif path.suffix == ".pxd":

            return parse_cython_pxd(path)

        elif path.suffix == ".pxi":

            return None

        else:

            return None

    except Exception as e:

        print(f"FAILED: {path}")
        print(type(e).__name__)
        print(e)

        return None