from dataclasses import dataclass, field


@dataclass
class Variable:

    name: str
    type_name: str
    value: str | None = None


@dataclass
class SymbolTable:

    variables: dict[str, Variable] = field(
        default_factory=dict
    )