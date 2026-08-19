from pathlib import Path

from transpiler_custom.models.imports import (
    ImportNode,
    ResolvedImportNode,
)


SKLEARN_ROOT = Path.cwd() / "sklearn"


def resolve_import(import_node: ImportNode) -> ResolvedImportNode:

    module = resolve_module_name(import_node)

    module_file = find_module_file(
        module,
        import_node.is_cimport,
    )

    return ResolvedImportNode(
        original=import_node,
        resolved_module=module,
        module_file=module_file,
        symbol_files=[],
        external=module_file is None,
    )


def resolve_module_name(import_node: ImportNode) -> str:

    if import_node.level == 0:

        return import_node.module

    source = Path(import_node.source_file)

    package = source.parent.parts

    prefix = package[:-import_node.level]

    if import_node.module:

        return ".".join(
            (*prefix, *import_node.module.split("."))
        )

    return ".".join(prefix)


def find_module_file(
    module: str,
    is_cimport: bool,
) -> Path | None:

    parts = module.split(".")

    if parts[0] == "sklearn":

        parts = parts[1:]

    relative = Path(*parts)

    candidates = []

    if is_cimport:

        candidates.extend(
            [
                SKLEARN_ROOT / f"{relative}.pxd",
                SKLEARN_ROOT / f"{relative}.pyx",
                SKLEARN_ROOT / relative / "__init__.pxd",
                SKLEARN_ROOT / relative / "__init__.py",
            ]
        )

    else:

        candidates.extend(
            [
                SKLEARN_ROOT / f"{relative}.py",
                SKLEARN_ROOT / f"{relative}.pyx",
                SKLEARN_ROOT / relative / "__init__.py",
            ]
        )

    for candidate in candidates:

        if candidate.exists():

            return candidate.relative_to(Path.cwd())

    return None