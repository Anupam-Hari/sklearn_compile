from pathlib import Path

from transpiler.dependency.models import (
    DependencyGraph,
    ResolvedDependency,
    Symbol,
)


def find_imported_symbol(
    graph: DependencyGraph,
    file_path: Path,
    name: str,
) -> Symbol | None:

    for symbol in graph.symbols.get(
        file_path,
        [],
    ):

        if symbol.name == name:

            return symbol

    return None

def find_import_by_name(
    graph: DependencyGraph,
    file_path: Path,
    name: str,
):

    for imported in graph.imports.get(
        file_path,
        [],
    ):

        if imported.name == name:

            return imported

    return None


def build_import_index(
    graph: DependencyGraph,
) -> dict[str, Path]:

    modules = {}

    for path in graph.files:

        module = path.as_posix()

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
                    :-len(suffix)
                ]

                break

        if module.endswith(
            ".__init__",
        ):

            module = module[:-9]

        modules[module] = path

    return modules

def resolve_module_path(
    graph,
    current_file,
    module,
    level,
):

    if level == 0:

        return graph.import_index.get(
            module,
        )

    parts = current_file.as_posix().split("/")

    package = parts[:-1]

    package = package[:-(level - 1)]

    if module:

        package.extend(
            module.split(".")
        )

    resolved_module = ".".join(
        package,
    )

    return graph.import_index.get(
        resolved_module,
    )


def resolve_import_symbol(
    graph: DependencyGraph,
    imported,
    current_file=None,
    visited=None,
) -> Symbol | None:

    if visited is None:

        visited = set()

    key = (
        current_file,
        imported.module,
        imported.name,
        imported.level,
    )

    if key in visited:
    
        return None

    visited.add(
        key,
    )

    if imported.name is None:

        return None

    if imported.level:

        source_file = resolve_module_path(
            graph,
            current_file,
            imported.module,
            imported.level,
        )

    else:

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

    nested_import = find_import_by_name(
        graph,
        source_file,
        imported.name,
    )

    if nested_import is None:

        return None

    return resolve_import_symbol(
        graph,
        nested_import,
        current_file=source_file,
        visited=visited,
    )


def resolve_file_imports(
    graph: DependencyGraph,
    file_path: Path,
) -> list[Symbol]:

    dependencies = []

    imports = graph.imports.get(
        file_path,
        [],
    )

    for imported in imports:

        symbol = resolve_import_symbol(
            graph,
            imported,
            current_file=file_path,
        )

        if symbol is not None:

            dependencies.append(
                symbol,
            )

    return dependencies


def build_import_tree(
    graph: DependencyGraph,
    file_path: Path,
    visited: set | None = None,
) -> list[Symbol]:

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


def resolve_imports(
    graph: DependencyGraph,
) -> None:

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
                current_file=file_path,
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