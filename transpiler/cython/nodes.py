from dataclasses import dataclass, field


@dataclass
class CythonNode:
    pass


@dataclass
class BlockNode(CythonNode):

    kind: str

    condition: str = ""

    children: list["CythonNode"] = field(
        default_factory=list
    )


@dataclass
class CallNode(CythonNode):

    name: str


@dataclass
class ReturnNode(CythonNode):

    value: str

@dataclass
class RaiseNode:
    exception: str

@dataclass
class AssignmentNode:
    target: str
    value: str