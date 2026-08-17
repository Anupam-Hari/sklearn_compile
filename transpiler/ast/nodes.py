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
            children=[],
        )

        self.imports = []
        self.classes = []
        self.functions = []
        self.calls = []

        self.variables = []
        self.constants = []
        self.typedefs = []
        self.structs = []
        self.enums = []
        self.externs = []

        for child in children or []:

            self.add_child(child)

    def add_child(self, child):

        self.children.append(child)

        node_type = getattr(
            child,
            "node_type",
            None,
        )

        if node_type == "import":

            self.imports.append(child)

        elif node_type == "class":

            self.classes.append(child)

        elif node_type == "function":

            self.functions.append(child)

        elif node_type == "call":

            self.calls.append(child)

        elif node_type == "variable":

            self.variables.append(child)

        elif node_type == "constant":

            self.constants.append(child)

        elif node_type == "typedef":

            self.typedefs.append(child)

        elif node_type == "struct":

            self.structs.append(child)

        elif node_type == "enum":

            self.enums.append(child)

        elif node_type == "extern":

            self.externs.append(child)


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
class CallNode(ASTNode):

    name: str = ""

    node_type: str = "call"


@dataclass
class FunctionNode(ASTNode):
    def __init__(self, name: str, attributes: dict | None = None, children: list[ASTNode] | None = None):
        super().__init__(node_type="function", name=name, attributes=attributes or {}, children=children or [])


@dataclass
class VariableNode(ASTNode):
    def __init__(self, name: str, attributes: dict | None = None, children: list[ASTNode] | None = None):
        super().__init__(node_type="variable", name=name, attributes=attributes or {}, children=children or [])

@dataclass
class ConstantNode(ASTNode):

    def __init__(
        self,
        name,
        value=None,
    ):

        super().__init__(
            node_type="constant",
            name=name,
            attributes={
                "value": value,
            },
        )

        self.value = value

@dataclass
class StructNode(ASTNode):

    def __init__(
        self,
        name,
        attributes=None,
        children=None,
    ):

        super().__init__(
            node_type="struct",
            name=name,
            attributes=attributes or {},
            children=children or [],
        )

@dataclass
class EnumNode(ASTNode):

    def __init__(
        self,
        name,
        attributes=None,
        children=None,
    ):

        super().__init__(
            node_type="enum",
            name=name,
            attributes=attributes or {},
            children=children or [],
        )

@dataclass
class ExpressionNode(ASTNode):

    def __init__(
        self,
        name=None,
        attributes=None,
        children=None,
    ):

        super().__init__(
            node_type="expression",
            name=name,
            attributes=attributes or {},
            children=children or [],
        )

@dataclass
class AttributeNode(ASTNode):

    def __init__(
        self,
        name,
        value=None,
    ):

        super().__init__(
            node_type="attribute",
            name=name,
            attributes={
                "value": value,
            },
        )

        self.value = value

@dataclass
class CompareNode(ASTNode):

    def __init__(
        self,
        operator=None,
        left=None,
        right=None,
    ):

        super().__init__(
            node_type="compare",
            name=operator,
            attributes={
                "left": left,
                "right": right,
            },
        )

@dataclass
class BinaryOperationNode(ASTNode):

    def __init__(
        self,
        operator=None,
        left=None,
        right=None,
    ):

        super().__init__(
            node_type="binary_operation",
            name=operator,
            attributes={
                "left": left,
                "right": right,
            },
        )

@dataclass
class UnaryOperationNode(ASTNode):

    def __init__(
        self,
        operator=None,
        operand=None,
    ):

        super().__init__(
            node_type="unary_operation",
            name=operator,
            attributes={
                "operand": operand,
            },
        )

@dataclass
class ListNode(ASTNode):

    def __init__(self, children=None):

        super().__init__(
            node_type="list",
            children=children or [],
        )


@dataclass
class TupleNode(ASTNode):

    def __init__(self, children=None):

        super().__init__(
            node_type="tuple",
            children=children or [],
        )


@dataclass
class DictNode(ASTNode):

    def __init__(self, children=None):

        super().__init__(
            node_type="dict",
            children=children or [],
        )


@dataclass
class SetNode(ASTNode):

    def __init__(self, children=None):

        super().__init__(
            node_type="set",
            children=children or [],
        )

@dataclass
class IndexNode(ASTNode):

    def __init__(
        self,
        value=None,
        index=None,
    ):

        super().__init__(
            node_type="index",
            attributes={
                "value": value,
                "index": index,
            },
        )

@dataclass
class SliceNode(ASTNode):

    def __init__(
        self,
        start=None,
        stop=None,
        step=None,
    ):

        super().__init__(
            node_type="slice",
            attributes={
                "start": start,
                "stop": stop,
                "step": step,
            },
        )

@dataclass
class TypeDefNode(ASTNode):

    def __init__(self, name):

        super().__init__(
            node_type="typedef",
            name=name,
        )

@dataclass
class TypeDefNode(ASTNode):

    def __init__(self, name):

        super().__init__(
            node_type="typedef",
            name=name,
        )

@dataclass
class ExternNode(ASTNode):

    def __init__(self, name):

        super().__init__(
            node_type="extern",
            name=name,
        )

@dataclass
class ParameterNode(ASTNode):

    def __init__(
        self,
        name,
        type_name=None,
    ):

        super().__init__(
            node_type="parameter",
            name=name,
            attributes={
                "type": type_name,
            },
        )

#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
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

@dataclass
class RaiseNode(ASTNode):

    def __init__(
        self,
        exception: str | None = None,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):

        super().__init__(
            node_type="raise",
            name="raise",
            attributes={
                **(attributes or {}),
                "exception": exception,
            },
            children=children or [],
        )

        self.exception = exception


@dataclass
class BreakNode(ASTNode):

    def __init__(
        self,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):

        super().__init__(
            node_type="break",
            name="break",
            attributes=attributes or {},
            children=children or [],
        )


@dataclass
class ContinueNode(ASTNode):

    def __init__(
        self,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):

        super().__init__(
            node_type="continue",
            name="continue",
            attributes=attributes or {},
            children=children or [],
        )


@dataclass
class PassNode(ASTNode):

    def __init__(
        self,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):

        super().__init__(
            node_type="pass",
            name="pass",
            attributes=attributes or {},
            children=children or [],
        )


@dataclass
class WithNode(ASTNode):

    def __init__(
        self,
        context: str | None = None,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):

        super().__init__(
            node_type="with",
            name="with",
            attributes={
                **(attributes or {}),
                "context": context,
            },
            children=children or [],
        )

        self.context = context


@dataclass
class TryNode(ASTNode):

    def __init__(
        self,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):

        super().__init__(
            node_type="try",
            name="try",
            attributes=attributes or {},
            children=children or [],
        )


@dataclass
class ExceptNode(ASTNode):

    def __init__(
        self,
        exception_type: str | None = None,
        attributes: dict | None = None,
        children: list[ASTNode] | None = None,
    ):

        super().__init__(
            node_type="except",
            name="except",
            attributes={
                **(attributes or {}),
                "exception_type": exception_type,
            },
            children=children or [],
        )

        self.exception_type = exception_type