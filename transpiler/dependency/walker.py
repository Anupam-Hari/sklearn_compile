from pathlib import Path

from transpiler.dependency.instantiations import (
    extract_instantiations,
)
from transpiler.dependency.method_calls import (
    extract_method_calls,
)
from transpiler.dependency.resolver import (
    find_symbol,
)
from transpiler.project.analyze import (
    analyze_project,
)
from transpiler.dependency.filter import (
    keep_dependency,
)

def walk_method(
    root: Path,
    class_name: str,
    method_name: str,
):

    graph = analyze_project(root)

    symbol = find_symbol(
        graph,
        class_name,
    )

    if symbol is None:

        print(
            f"{class_name} not found"
        )

        return

    print()

    print(
        f"{class_name}.{method_name}"
    )

    path = symbol.file_path

    instances = extract_instantiations(path)

    methods = extract_method_calls(path)

    for variable, called_method in methods.get(
        method_name,
        [],
    ):
        if not keep_dependency(
            variable,
            called_method,
        ):
            continue

        print()

        print(
            f"{variable}.{called_method}"
        )

        if variable in instances:

            for cls in instances[variable]:

                resolved = find_symbol(
                    graph,
                    cls,
                )

                print(
                    f"    {cls}"
                )

                print(
                    f"        {resolved}"
                )