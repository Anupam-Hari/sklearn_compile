from pathlib import Path

from transpiler.dependency.models import DependencyGraph, ResolvedDependency
from transpiler.dependency.models import Symbol


def find_symbol(
    graph: DependencyGraph,
    name: str,
) -> Symbol | None:

    for symbols in graph.symbols.values():

        for symbol in symbols:

            if symbol.name == name:
                return symbol

    return None


def find_symbols_in_file(
    graph: DependencyGraph,
    file_path: Path,
) -> list[Symbol]:

    return graph.symbols.get(file_path, [])

def resolve_import(
    graph,
    import_symbol,
):

    if import_symbol.name is None:
        return None

    return find_symbol(
        graph,
        import_symbol.name,
    )

def resolve_file_dependencies(
    graph,
    file_path,
):

    dependencies = []

    imports = graph.imports.get(
        file_path,
        [],
    )

    found = 0
    not_found = 0
    unresolved = []

    for imported_symbol in imports:

        symbol = resolve_import(
            graph,
            imported_symbol,
        )

        if symbol:

            found += 1

            dependencies.append(
                symbol,
            )

        else:

            not_found += 1
            unresolved.append(
                f"{imported_symbol.module}.{imported_symbol.name}"
            )

    print(
        f"{file_path}: "
        f"{found} resolved, "
        f"{not_found} unresolved "
        f"({len(imports)} total imports)"
    )

    if unresolved:

        print("    Missing:")

        for name in unresolved:

            print(f"        {name}")

        return dependencies

def build_dependency_tree(
    graph,
    file_path,
    visited=None,
):

    if visited is None:

        visited = set()

    if file_path in visited:

        return []

    print(f"VISITING: {file_path}")

    visited.add(
        file_path,
    )

    dependencies = []

    direct_dependencies = (
        resolve_file_dependencies(
            graph,
            file_path,
        )
    )

    print(
            f"FOUND {len(direct_dependencies)} "
            f"DEPENDENCIES"
        )

    for dependency in direct_dependencies:

        print(
            f"    {dependency.name}"
            f" -> "
            f"{dependency.file_path}"
        )

        dependencies.append(
            dependency,
        )

        dependencies.extend(

            build_dependency_tree(

                graph,

                dependency.file_path,

                visited,
            )
        )

    return dependencies

def resolve_dependencies(
    graph: DependencyGraph,
):

    for file_path, imports in graph.imports.items():

        resolved = []

        for imported in imports:

            if imported.name is None:
                continue

            symbol = find_symbol(
                graph,
                imported.name,
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