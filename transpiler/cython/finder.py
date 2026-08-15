from pathlib import Path
import re


def find_class(path: str | Path, class_name: str):

    source = Path(path).read_text()

    pattern = rf"cdef\s+class\s+{re.escape(class_name)}"

    match = re.search(pattern, source)

    if not match:
        return None

    return match.start()