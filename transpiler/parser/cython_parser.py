from pathlib import Path


def parse_cython_file(
    path: str | Path,
) -> str:

    path = Path(path)

    with open(path, "r") as f:
        return f.read()