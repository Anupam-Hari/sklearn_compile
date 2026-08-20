from pathlib import Path

from transpiler.parser.python_parser import (
    parse_python_file,
)
from transpiler.normalizer.python_normalizer import (
    normalize_python_ast,
)
from transpiler.dependency.calls import (
    extract_calls,
)

path = Path("sklearn/base.py")

tree = parse_python_file(path)

module = normalize_python_ast(tree)

print(f"Module: {path}")
print(f"Top-level functions: {len(module.functions)}")
print(f"Top-level calls: {len(module.calls)}")

print("\n" + "=" * 80)
print("FUNCTION CALL COUNTS")
print("=" * 80)

for function in module.functions:

    calls = extract_calls(function)

    print(
        f"{function.name:<40}"
        f"{len(calls)}"
    )

print("\n" + "=" * 80)
print("FIRST 50 CALLS")
print("=" * 80)

calls = extract_calls(module)

for function in module.functions:

    print()

    print(function.name)

    for child in function.children[:10]:

        print(
            child.node_type,
            child.name,
        )