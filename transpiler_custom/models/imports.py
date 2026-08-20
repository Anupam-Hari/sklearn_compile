from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImportNode:

    module: str | None

    symbols: list[str]

    alias: dict[str, str]

    level: int

    is_cimport: bool

    source_file: Path


@dataclass
class ResolvedImportNode:

    original: ImportNode

    resolved_module: str | None

    module_file: Path | None

    symbol_files: list[Path]

    external: bool