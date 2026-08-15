from pathlib import Path

from transpiler.project.analyze import analyze_project
from transpiler.dependency.resolver import find_symbol
from transpiler.dependency.method_calls import extract_method_calls
from transpiler.cython.method_extractor import extract_method
from transpiler.cython.calls import extract_calls


def build_dependency_pipeline(project_root: Path):

    graph = analyze_project(project_root)

    count = 0

    for file_path, symbols in graph.symbols.items():

        for symbol in symbols:

            if symbol.name == "DecisionTreeClassifier":
                print("FOUND:", symbol)
                count += 1

    print("MATCHES:", count)

    tree_symbol = find_symbol(
        graph,
        "DecisionTreeClassifier",
    )

    print(tree_symbol)

    all_calls = extract_method_calls(
        tree_symbol.file_path,
    )

    calls = all_calls.get(
        "_fit",
        [],
    )

    for obj, method in calls:
        
        call = f"{obj}.{method}"

        print(call)

        if call == "builder.build":

            for builder in (
                "DepthFirstTreeBuilder",
                "BestFirstTreeBuilder",
            ):

                symbol = find_symbol(
                    graph,
                    builder,
                )

                if not symbol:
                    continue

                method = extract_method(
                    symbol.file_path,
                    builder,
                    "build",
                )

                if not method:
                    continue

                print()

                print(builder)

                for dependency in extract_calls(method):

                    print("   ", dependency)