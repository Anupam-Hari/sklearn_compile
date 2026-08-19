# transpiler_custom/project/build_index.py

from collections import deque
from pathlib import Path

from transpiler_custom.normalizer.normalize_imports import (
    normalize_imports,
)
from transpiler_custom.parser.parser import parse_file
from transpiler_custom.resolver.import_resolver import (
    resolve_import,
)

parsed_files = 0
resolved_files = 0
parse_errors = 0

def build_index(entry_file: str | Path):

    global parsed_files, resolved_files, parse_errors

    entry_file = Path(entry_file)

    discovered = set()

    queue = deque(
        [
            entry_file,
        ]
    )

    while queue:

        path = queue.popleft()

        if path in discovered:

            continue

        discovered.add(path)

        try:

            tree = parse_file(path)
            parsed_files+=1

        except Exception:
            
            parse_errors+=1
            continue

        imports = normalize_imports(
            tree,
            path,
        )

        for import_node in imports:

            resolved = resolve_import(import_node)

            if resolved.external:

                continue

            #resolved_files+=1
            if resolved.module_file not in discovered:

                queue.append(
                    resolved.module_file,
                )

    return sorted(discovered)


if __name__ == "__main__":

    files = build_index(
        "sklearn/ensemble/_forest.py",
    )

    print()

    for file in files:

        print(file)

    print(f"\nParsed files: {parsed_files}")
    #print(f"Resolved files: {resolved_files}")
    print(f"Parse errors: {parse_errors}")