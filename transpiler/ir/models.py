from dataclasses import dataclass, field
from typing import Any


@dataclass
class IROperation:
    opcode: str
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class IRModule:
    operations: list[IROperation] = field(default_factory=list)

    def add(self, operation: IROperation) -> None:
        self.operations.append(operation)