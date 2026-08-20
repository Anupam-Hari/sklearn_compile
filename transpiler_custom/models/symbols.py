from dataclasses import dataclass
from pathlib import Path


@dataclass
class SymbolNode:

    name: str

    kind: str

    source_file: Path

    parent_name: str | None = None

    parent_kind: str | None = None


@dataclass
class ResolvedSymbolNode:

    original: SymbolNode

    resolved_file: Path

    external: bool