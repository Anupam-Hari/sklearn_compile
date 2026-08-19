from collections import deque
from pathlib import Path

from transpiler_custom.models.dependencies import (
    FileDependencyNode,
)
from transpiler_custom.normalizer.normalize_imports import (
    normalize_imports,
)
from transpiler_custom.normalizer.normalize_symbols import (
    normalize_symbols,
)
from transpiler_custom.parser.parser import parse_file
from transpiler_custom.resolver.import_resolver import (
    resolve_import,
)

parsed_files = 0
parse_errors = 0


def build_index(entry_file: str | Path):

    global parsed_files, parse_errors

    entry_file = Path(entry_file)

    files = {}

    queue = deque([entry_file])

    while queue:

        path = queue.popleft()

        if path in files:

            continue

        try:

            tree = parse_file(path)
            parsed_files += 1

        except Exception:

            parse_errors += 1
            continue

        imports = normalize_imports(
            tree,
            path,
        )

        symbols = normalize_symbols(
            tree,
            path,
        )

        files[path] = FileDependencyNode(
            path=path,
            imports=imports,
            symbols=symbols,
        )

        for import_node in imports:

            resolved = resolve_import(import_node)

            if resolved.external:

                continue

            if resolved.original.symbols:

                next_files = resolved.symbol_files

            elif resolved.module_file:

                next_files = [
                    resolved.module_file,
                ]

            else:

                next_files = []

            for file in next_files:

                if file not in files:

                    queue.append(file)

    return files