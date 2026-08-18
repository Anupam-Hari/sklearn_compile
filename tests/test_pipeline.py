from pathlib import Path

from transpiler.project.analyze import analyze_project
from transpiler.resolver.import_resolver import resolve_imports
from transpiler.resolver.class_resolver import resolve_classes
from transpiler.resolver.inherited_member_resolver import (
    resolve_inherited_members,
)
from transpiler.resolver.call_resolver import (resolve_call, resolve_calls, resolve_self_call)


ROOT = Path("sklearn")


def print_section(title: str):

    print()
    print(title)
    print("=" * 80)


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

    for name, count in counter.most_common(50):

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

    print_class_resolution(graph)

    print_inherited_resolution(graph)

    print_call_resolution(graph)


if __name__ == "__main__":

    main()