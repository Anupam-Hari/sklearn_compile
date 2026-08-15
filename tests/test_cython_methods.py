from pathlib import Path

from transpiler.dependency.cython_methods import (
    extract_cython_methods,
)


methods = extract_cython_methods(
    Path(
        "sklearn/sklearn/tree/_tree.pyx"
    )
)

for cls, method_list in methods.items():

    if cls not in (
        "DepthFirstTreeBuilder",
        "BestFirstTreeBuilder",
    ):
        continue

    print()

    print(cls)

    for method in method_list:

        print("   ", method)