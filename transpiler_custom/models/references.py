from dataclasses import dataclass
from pathlib import Path

@dataclass
class ReferenceNode:

    name: str

    kind: str

    source_file: Path

@dataclass
class ResolvedReferenceNode:

    original: ReferenceNode

    resolved_symbol: str | None

    resolved_file: Path | None

    is_imported: bool

    is_local: bool

    is_builtin: bool

    external: bool