from pathlib import Path

from transpiler.dependency.instantiations import (
    extract_instantiations,
)

instances = extract_instantiations(
    Path("sklearn/sklearn/tree/_classes.py")
)

for variable, cls in instances.items():

    print(
        variable,
        "→",
        cls,
    )