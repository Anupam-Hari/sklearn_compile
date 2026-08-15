from pathlib import Path

from transpiler.cython.calls import extract_calls
from transpiler.cython.method_extractor import extract_method


path = Path(
    "sklearn/sklearn/tree/_tree.pyx"
)

method = extract_method(
    path,
    "DepthFirstTreeBuilder",
    "build",
)

calls = extract_calls(method)

for call in sorted(set(calls)):
    print(call)