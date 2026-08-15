from pathlib import Path

from transpiler.dependency.method_calls import (
    extract_method_calls,
)


calls = extract_method_calls(
    Path("sklearn/sklearn/tree/_classes.py")
)

for function, methods in calls.items():

    if function != "_fit":
        continue

    print(function)

    for obj, method in methods:

        print(obj, "->", method)