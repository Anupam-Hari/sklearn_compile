from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SourceFile:
    path: Path
    extension: str
    language: str


@dataclass
class ImportSymbol:
    module: str
    name: str | None = None


@dataclass
class Symbol:
    name: str
    symbol_type: str
    file_path: Path
    language: str
    parent: str | None = None
    line_number: int = 0


@dataclass
class DependencyGraph:
    files: dict[Path, SourceFile] = field(default_factory=dict)
    imports: dict[Path, list[ImportSymbol]] = field(default_factory=dict)
    symbols: dict[Path, list[Symbol]] = field(default_factory=dict)