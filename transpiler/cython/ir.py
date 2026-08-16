from transpiler.cython.statement_parser import (
    CythonStatementParser,
)


def build_cython_ir(method_source: str):

    parser = CythonStatementParser()

    return parser.parse(method_source)