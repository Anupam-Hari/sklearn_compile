# parser/utils.py

from pathlib import Path


def path_to_module(path: Path, project_root: Path) -> str:

    relative = path.relative_to(project_root)

    return ".".join(relative.with_suffix("").parts)