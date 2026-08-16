from pathlib import Path

from transpiler.cython.calls import extract_calls
from transpiler.cython.method_extractor import extract_method
from transpiler.symbols.builder import build_symbol_table


path = Path(
    "sklearn/sklearn/tree/_tree.pyx"
)

method = extract_method(
    path,
    "DepthFirstTreeBuilder",
    "build",
)


table = build_symbol_table(method)

for variable in table.variables.values():

    print(
        variable.name,
        variable.type_name,
    )