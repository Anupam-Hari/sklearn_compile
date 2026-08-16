from transpiler.symbols.models import (
    SymbolTable,
    Variable,
)

from transpiler.symbols.cython_variables import (
    extract_variables,
)


def build_symbol_table(source: str):

    table = SymbolTable()

    for name, type_name in extract_variables(
        source
    ):

        table.variables[name] = Variable(
            name=name,
            type_name=type_name,
        )

    return table