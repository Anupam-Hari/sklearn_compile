from dataclasses import dataclass, field


@dataclass
class ASTNode:
    node_type: str
    name: str | None = None
    children: list["ASTNode"] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)