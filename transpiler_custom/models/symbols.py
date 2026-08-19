from dataclasses import dataclass
from pathlib import Path


@dataclass
class SymbolNode:

    name: str

    kind: str

    source_file: Path