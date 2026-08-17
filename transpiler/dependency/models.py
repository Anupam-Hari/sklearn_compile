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
class Call:

    name: str

    parent_class: str | None = None

    parent_function: str | None = None


@dataclass
class DependencyGraph:

    files: dict = field(default_factory=dict)

    modules: dict = field(default_factory=dict)

    imports: dict = field(default_factory=dict)

    symbols: dict = field(default_factory=dict)

    dependencies: dict = field(default_factory=dict)

    calls: dict = field(default_factory=dict)

    import_index: dict = field(default_factory=dict)

    class_index: dict = field(default_factory=dict)

    function_index: dict = field(default_factory=dict)

    class_inheritance: dict = field(default_factory=dict)

    resolved_calls: dict = field(default_factory=dict)

    inherited_members: dict = field(default_factory=dict)

@dataclass
class ResolvedDependency:

    imported_name: str

    imported_from: str

    source_file: Path

    symbol_type: str