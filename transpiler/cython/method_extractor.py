from pathlib import Path


def extract_method(
    path: str | Path,
    class_name: str,
    method_name: str,
):

    lines = Path(path).read_text().splitlines()

    class_start = None

    for i, line in enumerate(lines):

        if line.startswith(f"cdef class {class_name}"):
            class_start = i
            break

    if class_start is None:
        return None

    method_start = None
    method_indent = None

    for i in range(class_start + 1, len(lines)):

        line = lines[i]

        stripped = line.lstrip()

        if line.startswith("cdef class "):
            break

        if (
            stripped.startswith(f"cpdef {method_name}(")
            or stripped.startswith(f"cdef {method_name}(")
            or stripped.startswith(f"def {method_name}(")
        ):
            method_start = i
            method_indent = len(line) - len(stripped)
            break

    if method_start is None:
        return None

    collected = []

    for i in range(method_start, len(lines)):

        line = lines[i]
        stripped = line.lstrip()

        current_indent = len(line) - len(stripped)

        if (
            i > method_start
            and current_indent <= method_indent
            and stripped
            and (
                stripped.startswith("cpdef ")
                or stripped.startswith("cdef class ")
                or stripped.startswith("def ")
            )
        ):
            break

        collected.append(line)

    return "\n".join(collected)