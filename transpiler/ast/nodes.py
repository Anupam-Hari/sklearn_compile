from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ASTNode:
    node_type: str
    name: str | None = None
    attributes: dict = field(default_factory=dict)
    children: list["ASTNode"] = field(default_factory=list)


@dataclass
class ModuleNode(ASTNode):

    def __init__(
        self,
        name=None,
        attributes=None,
        children=None,
    ):
        super().__init__(
            node_type="module",
            name=name,
            attributes=attributes or {},
            children=children or [],
        )
        self.imports: list[ImportNode] = []
        self.classes: list[ClassNode] = []
        self.functions: list[FunctionNode] = []
        self.children = list(children or [])
        for child in self.children:
            if getattr(child, "node_type", None) == "import":
                self.imports.append(child)
            elif getattr(child, "node_type", None) == "class":
                self.classes.append(child)
            elif getattr(child, "node_type", None) == "function":
                self.functions.append(child)


@dataclass
class ImportNode(ASTNode):
    def __init__(self, module: str = "", names: list[str] | None = None, attributes: dict | None = None, children: list[ASTNode] | None = None):
        super().__init__(node_type="import", name=module, attributes={**(attributes or {}), "names": names or []}, children=children or [])
        self.module = module
        self.names = names or []


@dataclass
class ClassNode(ASTNode):
    def __init__(self, name: str, bases: list[str] | None = None, methods: list["FunctionNode"] | None = None, attributes: dict | None = None, children: list[ASTNode] | None = None):
        super().__init__(node_type="class", name=name, attributes={**(attributes or {}), "bases": bases or []}, children=children or [])
        self.bases = bases or []
        self.methods = methods or []
        self.children.extend(self.methods)


@dataclass
class FunctionNode(ASTNode):
    def __init__(self, name: str, attributes: dict | None = None, children: list[ASTNode] | None = None):
        super().__init__(node_type="function", name=name, attributes=attributes or {}, children=children or [])


@dataclass
class VariableNode(ASTNode):
    def __init__(self, name: str, attributes: dict | None = None, children: list[ASTNode] | None = None):
        super().__init__(node_type="variable", name=name, attributes=attributes or {}, children=children or [])


@dataclass
class AssignmentNode(ASTNode):
    def __init__(
        self,
        name: str,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):
        attrs = attributes or {}
        attrs["target"] = name

        super().__init__(
            node_type="assignment",
            name=name,
            attributes=attrs,
            children=children or [],
        )

@dataclass
class CallNode(ASTNode):
    def __init__(
        self,
        name: str,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):
        super().__init__(
            node_type="call",
            name=name,
            attributes=attributes or {},
            children=children or [],
        )

        self.attributes["name"] = name

@dataclass
class IfNode(ASTNode):

    def __init__(
        self,
        condition: str | None = None,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):
        super().__init__(
            node_type="if",
            name="if",
            attributes={
                **(attributes or {}),
                "condition": condition,
            },
            children=children or [],
        )

        self.condition = condition

@dataclass
class WhileNode(ASTNode):

    def __init__(
        self,
        condition: str | None = None,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):
        super().__init__(
            node_type="while",
            name="while",
            attributes={
                **(attributes or {}),
                "condition": condition,
            },
            children=children or [],
        )

        self.condition = condition

@dataclass
class ForNode(ASTNode):

    def __init__(
        self,
        target: str | None = None,
        iterator: str | None = None,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):
        super().__init__(
            node_type="for",
            name=target,
            attributes={
                **(attributes or {}),
                "target": target,
                "iterator": iterator,
            },
            children=children or [],
        )

        self.target = target
        self.iterator = iterator

@dataclass
class ReturnNode(ASTNode):

    def __init__(
        self,
        value: str | None = None,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):
        super().__init__(
            node_type="return",
            name="return",
            attributes={
                **(attributes or {}),
                "value": value,
            },
            children=children or [],
        )

        self.value = value