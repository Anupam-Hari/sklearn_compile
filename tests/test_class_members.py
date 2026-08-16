from pathlib import Path

from transpiler.dependency.class_type_map import (
    build_class_type_map,
)


types = build_class_type_map(
    Path(
        "sklearn/sklearn/tree/_splitter.pyx"
    ),
    "Splitter",
)

for variable, typ in sorted(
    types.items()
):

    print(
        variable,
        typ,
    )