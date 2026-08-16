from dataclasses import dataclass, field

from transpiler.ir.models import IROperation, IRModule


@dataclass
class IRGraph:
    """Alias for IRModule for backwards compatibility."""
    operations: list[IROperation] = field(default_factory=list)

    def add(self, operation: IROperation) -> None:
        self.operations.append(operation)

    def dump(self) -> None:
        for index, operation in enumerate(self.operations):
            print(f"{index}: {operation}")