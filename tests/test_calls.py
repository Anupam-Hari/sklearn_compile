from pathlib import Path

from transpiler.dependency.calls import (
    extract_function_calls,
)


calls = extract_function_calls(

    Path(
        "sklearn/sklearn/tree/_classes.py"
    )

)

for function, dependencies in calls.items():

    print()

    print(function)

    for dependency in dependencies:

        print(
            "   ",
            dependency,
        )