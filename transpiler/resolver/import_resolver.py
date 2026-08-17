from pathlib import Path

from transpiler.dependency.models import (
    DependencyGraph,
    ResolvedDependency,
    Symbol,
)

def find_imported_symbol(
    graph,
    file_path,
    name,
):

    for symbol in graph.symbols.get(
        file_path,
        [],
    ):

        if symbol.name == name:

            return symbol

    return None


def build_import_index(graph):

    modules = {}

    for path in graph.files:

        module = str(path)

        module = module.replace(
            "/",
            ".",
        )

        for suffix in (
            ".py",
            ".pyx",
            ".pxd",
        ):

            if module.endswith(
                suffix,
            ):

                module = module[
                    : -len(suffix)
                ]

                break

        if module.endswith(
            ".__init__",
        ):

            module = module[:-9]

        modules[module] = path

    return modules


def resolve_import_symbol(
    graph,
    imported,
    visited=None,
):

    if visited is None:

        visited = set()

    key = (
        imported.module,
        imported.name,
    )

    if key in visited:

        return None

    visited.add(key)

    if imported.name is None:

        return None

    source_file = graph.import_index.get(
        imported.module,
    )

    if source_file is None:

        return None

    symbol = find_imported_symbol(
        graph,
        source_file,
        imported.name,
    )

    if symbol is not None:

        return symbol

    for nested_import in graph.imports.get(
        source_file,
        [],
    ):

        if nested_import.name != imported.name:

            continue

        symbol = resolve_import_symbol(
            graph,
            nested_import,
            visited,
        )

        if symbol is not None:

            return symbol

    return None


def resolve_file_imports(
    graph,
    file_path,
):

    dependencies = []

    imports = graph.imports.get(
        file_path,
        [],
    )

    for imported in imports:

        symbol = resolve_import_symbol(
            graph,
            imported,
        )

        if symbol is not None:

            dependencies.append(
                symbol,
            )

    return dependencies


def build_import_tree(
    graph,
    file_path,
    visited=None,
):

    if visited is None:

        visited = set()

    if file_path in visited:

        return []

    visited.add(
        file_path,
    )

    dependencies = []

    direct_dependencies = (
        resolve_file_imports(
            graph,
            file_path,
        )
    )

    for dependency in direct_dependencies:

        dependencies.append(
            dependency,
        )

        dependencies.extend(

            build_import_tree(

                graph,

                dependency.file_path,

                visited,
            )
        )

    return dependencies


def resolve_imports(graph):

    graph.import_index = (
        build_import_index(
            graph,
        )
    )

    for file_path, imports in (
        graph.imports.items()
    ):

        resolved = []

        for imported in imports:

            symbol = resolve_import_symbol(

                graph,

                imported,
            )

            if symbol is None:

                continue

            resolved.append(

                ResolvedDependency(

                    imported_name=imported.name,

                    imported_from=imported.module,

                    source_file=symbol.file_path,

                    symbol_type=symbol.symbol_type,
                )
            )

        graph.dependencies[
            file_path
        ] = resolved