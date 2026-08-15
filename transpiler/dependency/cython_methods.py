import re
from pathlib import Path


METHOD_PATTERN = re.compile(
    r"(?:cdef|cpdef|def)\s+([^\n]*?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
)


CLASS_PATTERN = re.compile(
    r"cdef\s+class\s+([A-Za-z_][A-Za-z0-9_]*)"
)


def extract_cython_methods(path: Path):

    lines = path.read_text().splitlines()

    methods = {}

    current_class = None

    for line in lines:

        class_match = CLASS_PATTERN.search(line)

        if class_match:

            current_class = class_match.group(1)

            methods[current_class] = []

            continue

        method_match = METHOD_PATTERN.search(line)

        if method_match and current_class:

            methods[current_class].append(
                method_match.group(2)
            )

    return methods