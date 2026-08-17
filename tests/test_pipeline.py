from pathlib import Path

from transpiler.project.analyze import analyze_project
from transpiler.resolver.import_resolver import resolve_imports, resolve_import_symbol
from transpiler.resolver.class_resolver import resolve_classes
from transpiler.resolver.inherited_member_resolver import (
    resolve_inherited_members,
)
from transpiler.resolver.call_resolver import (resolve_call, resolve_calls, resolve_self_call)


ROOT = Path("sklearn")

DEBUG_IMPORTS = True
DEBUG_CALLS = False

DEBUG_IMPORT_TARGET = None
# DEBUG_IMPORT_TARGET = "sklearn.utils.metadata_routing"

DEBUG_CALL_TARGET = None
# DEBUG_CALL_TARGET = "check_is_fitted"

TOP_N = 20

def debug_import(graph, target):

    print_section(
        f"IMPORT DEBUG: {target}"
    )

    for file_path, imports in graph.imports.items():

        for imported in imports:

            if imported.name:

                name = (
                    f"{imported.module}."
                    f"{imported.name}"
                )

            else:

                name = imported.module

            if name != target:

                continue

            print()
            print(f"FILE: {file_path}")
            print(f"IMPORT: {name}")

            symbol = resolve_import_symbol(
                graph,
                imported,
            )

            print(f"RESOLVED: {symbol}")

def debug_call(graph, target):

    print_section(
        f"CALL DEBUG: {target}"
    )

    for file_path, calls in graph.calls.items():

        for call in calls:

            if call.name != target:

                continue

            print()
            print(f"FILE: {file_path}")
            print(f"CALL: {call.name}")
            print(
                f"CLASS: {call.parent_class}"
            )
            print(
                f"FUNCTION: {call.parent_function}"
            )

def print_section(title: str):

    print()
    print(title)
    print("=" * 80)

def print_unresolved_imports(graph):

    from collections import Counter

    counter = Counter()

    for imports in graph.imports.values():

        for imported in imports:

            symbol = resolve_import_symbol(
                graph,
                imported,
            )

            if symbol is None:

                if imported.name:

                    name = (
                        f"{imported.module}."
                        f"{imported.name}"
                    )

                else:

                    name = imported.module

                counter[name] += 1

    print_section(
        "TOP UNRESOLVED IMPORTS"
    )

    for name, count in counter.most_common(TOP_N):

        if not (
            name.startswith("sklearn")
            or name.startswith("_")
        ):
            continue

        print(
            f"{count:<5}{name}"
        )

def print_unresolved_import_breakdown(graph):

    from collections import Counter

    categories = Counter()

    for file_path, imports in graph.imports.items():

        for imported in imports:

            if resolve_import_symbol(
                graph,
                imported,
                current_file=file_path,
            ) is not None:

                continue

            module = imported.module

            if module.startswith("sklearn"):

                categories["sklearn"] += 1

            elif module.startswith("_"):

                categories["relative"] += 1

            elif "." in module:

                categories["third_party.submodule"] += 1

            else:

                categories["third_party.top_level"] += 1

    print_section(
        "UNRESOLVED IMPORT BREAKDOWN"
    )

    for name, count in sorted(
        categories.items()
    ):

        print(
            f"{name:<25}{count}"
        )


def print_internal_unresolved_imports(graph):

    from collections import Counter

    counter = Counter()

    for file_path, imports in graph.imports.items():

        for imported in imports:

            if resolve_import_symbol(
                graph,
                imported,
                current_file=file_path,
            ) is not None:

                continue

            if not (
                imported.module.startswith("sklearn")
                or imported.module.startswith("_")
            ):

                continue

            if imported.name:

                name = (
                    f"{imported.module}."
                    f"{imported.name}"
                )

            else:

                name = imported.module

            counter[name] += 1

    print_section(
        "TOP INTERNAL UNRESOLVED IMPORTS"
    )

    for name, count in counter.most_common(50):

        print(
            f"{count:<5}{name}"
        )

def count_imports(graph):

    return sum(
        len(imports)
        for imports in graph.imports.values()
    )


def count_symbols(graph):

    return sum(
        len(symbols)
        for symbols in graph.symbols.values()
    )


def print_symbol_summary(graph):

    print_section("SYMBOL TYPES")

    counts = {}

    for symbols in graph.symbols.values():

        for symbol in symbols:

            counts[symbol.symbol_type] = (
                counts.get(
                    symbol.symbol_type,
                    0,
                )
                + 1
            )

    for symbol_type, count in sorted(
        counts.items()
    ):

        print(
            f"{symbol_type:<15}"
            f"{count}"
        )


def print_import_resolution(graph):

    print_section("IMPORT RESOLUTION")

    resolve_imports(graph)

    total = sum(
        len(imports)
        for imports in graph.imports.values()
    )

    resolved = sum(
        len(dependencies)
        for dependencies in graph.dependencies.values()
    )

    unresolved = total - resolved

    coverage = (
        resolved / total * 100
        if total
        else 0
    )

    print(f"total imports:      {total}")
    print(f"resolved imports:   {resolved}")
    print(f"unresolved imports: {unresolved}")
    print(f"coverage:           {coverage:.2f}%")

    print_unresolved_import_breakdown(
        graph,
    )

def print_class_resolution(graph):

    print_section(
        "CLASS RESOLUTION"
    )

    resolve_classes(graph)

    print(
        f"resolved classes:    "
        f"{len(graph.class_inheritance)}"
    )


def print_inherited_resolution(graph):

    print_section(
        "INHERITED MEMBER RESOLUTION"
    )

    resolve_inherited_members(
        graph
    )

    print(
        f"resolved members:    "
        f"{len(graph.inherited_members)}"
    )


def print_call_resolution(graph):

    from collections import Counter


    print_section(
        "CALL RESOLUTION"
    )

    counter = Counter()

    for calls in graph.calls.values():

        for call in calls:

            resolved = False

            if "." not in call.name:

                resolved = (
                    resolve_call(
                        graph,
                        call.name,
                    )
                    is not None
                )

            elif (
                call.name.startswith(
                    "self."
                )
                and call.parent_class
            ):

                resolved = (
                    resolve_self_call(
                        graph,
                        call.parent_class,
                        call.name,
                    )
                    is not None
                )

            if not resolved:

                counter[call.name] += 1

    resolve_calls(graph)

    # for file_path, calls in graph.calls.items():

    #     for call in calls:

    #         if call.name != "check_is_fitted":

    #             continue

    #         print()
    #         print("FILE:", file_path)

    #         print(
    #             "IMPORTS:",
    #             [
    #                 (
    #                     imported.module,
    #                     imported.name,
    #                 )
    #                 for imported in graph.imports.get(
    #                     file_path,
    #                     [],
    #                 )
    #             ],
    #         )

    #         print(
    #             "DEPENDENCIES:",
    #             [
    #                 dependency.imported_name
    #                 for dependency in graph.dependencies.get(
    #                     file_path,
    #                     [],
    #                 )
    #             ],
    #         )

    #         break

    total = sum(
        len(calls)
        for calls in graph.calls.values()
    )

    resolved = sum(
        len(calls)
        for calls in graph.resolved_calls.values()
    )

    unresolved = total - resolved

    coverage = (
        resolved / total * 100
        if total
        else 0
    )

    print(
        f"total calls:         {total}"
    )

    print(
        f"resolved calls:      {resolved}"
    )

    print(
        f"unresolved calls:    {unresolved}"
    )

    print(
        f"coverage:            {coverage:.2f}%"
    )

    print()

    print(
        "TOP UNRESOLVED CALLS"
    )

    print(
        "=" * 80
    )

    for name, count in counter.most_common(TOP_N):

        print(
            f"{count:<5}{name}"
        )


def main():

    graph = analyze_project(ROOT)

    print_section(
        "PROJECT SUMMARY"
    )

    print(
        f"files:               {len(graph.files)}"
    )

    print(
        f"imports:             {count_imports(graph)}"
    )

    print(
        f"symbols:             {count_symbols(graph)}"
    )

    print_symbol_summary(graph)

    print_import_resolution(graph)

    print_internal_unresolved_imports(
        graph,
    )

    print_class_resolution(graph)

    print_inherited_resolution(graph)

    print_call_resolution(graph)

    if DEBUG_IMPORTS and DEBUG_IMPORT_TARGET:

        debug_import(
            graph,
            DEBUG_IMPORT_TARGET,
        )

    if DEBUG_CALLS and DEBUG_CALL_TARGET:

        debug_call(
            graph,
            DEBUG_CALL_TARGET,
        )


if __name__ == "__main__":

    main()