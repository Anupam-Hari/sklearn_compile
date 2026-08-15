from pathlib import Path

from transpiler.cython.calls import extract_calls
from transpiler.cython.dependency_graph import build_dependency_graph
from transpiler.cython.method_extractor import extract_method


method = extract_method(
    Path("sklearn/sklearn/tree/_tree.pyx"),
    "DepthFirstTreeBuilder",
    "build",
)

calls = extract_calls(method)

graph = build_dependency_graph(calls)

for name, data in graph.items():

    print(
        f"{name} -> {data['type']}"
    )