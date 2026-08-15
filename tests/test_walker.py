from pathlib import Path

from transpiler.dependency.walker import (
    walk_method,
)


walk_method(
    Path("sklearn/sklearn/tree"),
    "DecisionTreeClassifier",
    "_fit",
)