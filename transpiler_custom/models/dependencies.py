from dataclasses import dataclass, field
from pathlib import Path

from transpiler_custom.models.imports import ImportNode
from transpiler_custom.models.symbols import SymbolNode


@dataclass
class FileDependencyNode:

    path: Path

    imports: list[ImportNode] = field(default_factory=list)

    symbols: list[SymbolNode] = field(default_factory=list)