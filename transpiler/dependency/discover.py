from pathlib import Path

from .models import SourceFile


SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".pyx": "cython",
    ".pxd": "cython",
    ".pxi": "cython",
}


def discover_source_files(root: Path) -> list[SourceFile]:
    source_files: list[SourceFile] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix not in SUPPORTED_EXTENSIONS:
            continue

        source_files.append(
            SourceFile(
                path=path.resolve(),
                extension=path.suffix,
                language=SUPPORTED_EXTENSIONS[path.suffix],
            )
        )

    return sorted(source_files, key=lambda f: str(f.path))