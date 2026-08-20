from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

class FileType(Enum):
    PYTHON = "py"
    CYTHON = "pyx"
    CYTHON_HEADER = "pxd"


@dataclass
class ParsedFile:
    path: Path
    source: str
    tree: Any
    file_type: FileType