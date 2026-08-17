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
    base_classes: list[str] | None = None

    inherited_from: str | None = None

    line_number: int = 0


@dataclass
class DependencyGraph:

    files: dict = field(
        default_factory=dict
    )

    imports: dict = field(
        default_factory=dict
    )

    symbols: dict = field(
        default_factory=dict
    )

    dependencies: dict = field(
        default_factory=dict
    )

@dataclass
class ResolvedDependency:

    imported_name: str

    imported_from: str

    source_file: Path

    symbol_type: str