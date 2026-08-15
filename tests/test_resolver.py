from pathlib import Path

from transpiler.dependency.resolver import find_symbol
from transpiler.project.analyze import analyze_project


graph = analyze_project(
    Path("sklearn/sklearn/tree")
)

targets = [
    "DecisionTreeClassifier",
    "DepthFirstTreeBuilder",
    "BestFirstTreeBuilder",
]

for target in targets:

    symbol = find_symbol(
        graph,
        target,
    )

    print()

    print(target)

    print(symbol)