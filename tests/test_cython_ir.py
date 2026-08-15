from pathlib import Path

from transpiler.cython.method_extractor import extract_method
from transpiler.cython.visitor import CythonMethodVisitor


path = Path("sklearn/sklearn/tree/_tree.pyx")

method = extract_method(
    path,
    "DepthFirstTreeBuilder",
    "build",
)

print(len(method.splitlines()))

print("METHOD")
print("=" * 80)

print(method)

print()
print("IR")
print("=" * 80)

visitor = CythonMethodVisitor()

graph = visitor.visit(method)

for i, op in enumerate(graph.operations):
    print(f"{i}: {op}")