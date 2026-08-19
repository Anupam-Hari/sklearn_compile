from pathlib import Path

from transpiler_custom.models.imports import (
    ImportNode,
    ResolvedImportNode,
)
from transpiler_custom.normalizer.normalize_symbols import (
    normalize_symbols,
)
from transpiler_custom.normalizer.normalize_imports import (
    normalize_imports,
)
from transpiler_custom.parser.parser import parse_file


SKLEARN_ROOT = Path.cwd() / "sklearn"


def find_symbol_files(
    module_file,
    symbols,
    visited=None,
):

    if visited is None:

        visited = set()

    if not module_file:

        return []

    module_file = Path(module_file)

    if module_file in visited:

        return []

    visited.add(module_file)

    if not symbols:

        return []

    try:

        tree = parse_file(module_file)

    except Exception:

        return []

    files = set()

    normalized_symbols = normalize_symbols(
        tree,
        module_file,
    )

    symbol_map = {
        symbol.name: symbol.source_file
        for symbol in normalized_symbols
    }

    imports = normalize_imports(
        tree,
        module_file,
    )

    for symbol_name in symbols:

        # Symbol defined in this file
        if symbol_name in symbol_map:

            files.add(
                Path(symbol_map[symbol_name])
            )

            continue

        # Symbol re-exported from another file
        for import_node in imports:

            if symbol_name not in import_node.symbols and "*" not in import_node.symbols:

                continue

            module = resolve_module_name(
                import_node
            )

            # print(
            #     "\nFOLLOWING RE-EXPORT:"
            # )

            # print(
            #     "CURRENT FILE:",
            #     module_file,
            # )

            # print(
            #     "IMPORT:",
            #     import_node.module,
            # )

            # print(
            #     "LEVEL:",
            #     import_node.level,
            # )

            # print(
            #     "RESOLVED MODULE:",
            #     module,
            # )

            next_module_file = find_module_file(
                module,
                import_node.is_cimport,
            )

            # print(
            #     "NEXT FILE:",
            #     next_module_file,
            # )

            files.update(
                find_symbol_files(
                    next_module_file,
                    [symbol_name],
                    visited,
                )
            )

    return sorted(files)

def resolve_import(import_node: ImportNode,) -> ResolvedImportNode:

    module = resolve_module_name(import_node)

    module_file = find_module_file(
        module,
        import_node.is_cimport,
    )

    symbol_files = find_symbol_files(
        module_file,
        import_node.symbols,
    )

    if (
        module_file is not None
        and import_node.symbols
        and not symbol_files
    ):

        # print(
        #     "\nUNRESOLVED:",
        #     import_node.module,
        #     import_node.symbols,
        #     module_file,
        # )

        try:

            tree = parse_file(module_file)

            symbols = normalize_symbols(
                tree,
                module_file,
            )

            imports = normalize_imports(
                            tree,
                            module_file,
                        )

            # print("\nAVAILABLE SYMBOLS:\n")

            # for symbol in symbols:

            #     print(
            #         f"{symbol.kind:<20}"
            #         f"{symbol.name}"
            #     )

            # print("\nAVAILABLE IMPORTS:\n")

            # for imp in imports:

            #     print(
            #         imp.module,
            #         imp.symbols,
            #     )

        except Exception as e:

            print("\nFAILED TO PARSE:", e)

        # print("\n" + "=" * 80)

    return ResolvedImportNode(
        original=import_node,
        resolved_module=module,
        module_file=module_file,
        symbol_files=symbol_files,
        external=module_file is None,
    )


def resolve_module_name(
    import_node: ImportNode,
) -> str:

    if import_node.level == 0:

        return import_node.module

    source = Path(import_node.source_file)

    package = source.parent.parts

    if source.stem == "__init__":

        prefix = package[: -(import_node.level - 1)]

    else:

        prefix = package[: -import_node.level]

    if import_node.module:

        return ".".join(
            (
                *prefix,
                *import_node.module.split("."),
            )
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