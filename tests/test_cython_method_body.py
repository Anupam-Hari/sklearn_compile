from pathlib import Path

from transpiler.cython.method_extractor import extract_method


path = Path(
    "sklearn/sklearn/tree/_tree.pyx"
)

body = extract_method(
    path,
    "DepthFirstTreeBuilder",
    "build",
)

print(body)