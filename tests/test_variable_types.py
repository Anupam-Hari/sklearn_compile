from pathlib import Path

from transpiler.cython.variable_types import (
    extract_variable_types,
)


PATH = (
    Path("sklearn")
    / "sklearn"
    / "tree"
    / "_tree.pyx"
)


variables = extract_variable_types(PATH)

for name, variable_type in sorted(variables.items()):

    print(
        f"{name} -> {variable_type}"
    )