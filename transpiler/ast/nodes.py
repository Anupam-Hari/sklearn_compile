from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ASTNode:

    children: list["ASTNode"] = field(
        default_factory=list,
    )


@dataclass
class DeclarationNode(ASTNode):

    pass


@dataclass
class StatementNode(ASTNode):

    pass


@dataclass
class ExpressionNode(ASTNode):

    pass

@dataclass
class ModuleNode(DeclarationNode):

    name: str | None = None


@dataclass
class ImportNode(DeclarationNode):

    module: str = ""

    names: list[str] = field(
        default_factory=list,
    )


@dataclass
class ParameterNode(DeclarationNode):

    name: str = ""

    annotation: str | None = None

    default: str | None = None


@dataclass
class VariableNode(DeclarationNode):

    name: str = ""

    value: str | None = None


@dataclass
class FunctionNode(DeclarationNode):

    name: str = ""

    parameters: list[ParameterNode] = field(
        default_factory=list,
    )

    returns: str | None = None


@dataclass
class ClassNode(DeclarationNode):

    name: str = ""

    bases: list[str] = field(
        default_factory=list,
    )


@dataclass
class StructNode(DeclarationNode):

    name: str = ""


@dataclass
class EnumNode(DeclarationNode):

    name: str = ""


@dataclass
class TypeDefNode(DeclarationNode):

    name: str = ""


@dataclass
class ExternNode(DeclarationNode):

    name: str = ""

@dataclass
class AssignmentNode(StatementNode):

    target: str | None = None

    value: ExpressionNode | None = None


@dataclass
class ReturnNode(StatementNode):

    value: ExpressionNode | None = None


@dataclass
class RaiseNode(StatementNode):

    pass


@dataclass
class BreakNode(StatementNode):

    pass


@dataclass
class ContinueNode(StatementNode):

    pass


@dataclass
class PassNode(StatementNode):

    pass

@dataclass
class IfNode(StatementNode):

    pass


@dataclass
class ForNode(StatementNode):

    pass


@dataclass
class WhileNode(StatementNode):

    pass


@dataclass
class WithNode(StatementNode):

    pass


@dataclass
class ExceptNode(StatementNode):

    pass


@dataclass
class TryNode(StatementNode):

    pass

@dataclass
class CallNode(ExpressionNode):

    name: str = ""

    arguments: list[ExpressionNode] = field(
        default_factory=list,
    )

@dataclass
class AttributeNode(ExpressionNode):

    name: str = ""


@dataclass
class CompareNode(ExpressionNode):

    operator: str = ""


@dataclass
class BooleanNode(ExpressionNode):

    operator: str = ""


@dataclass
class BinaryOperationNode(ExpressionNode):

    operator: str = ""

    left: ExpressionNode | None = None

    right: ExpressionNode | None = None


@dataclass
class UnaryOperationNode(ExpressionNode):

    operator: str = ""

@dataclass
class ListNode(ExpressionNode):

    pass


@dataclass
class TupleNode(ExpressionNode):

    pass


@dataclass
class DictNode(ExpressionNode):

    pass


@dataclass
class SetNode(ExpressionNode):

    pass


@dataclass
class IndexNode(ExpressionNode):

    pass


@dataclass
class SliceNode(ExpressionNode):

    pass


@dataclass
class LiteralNode(ExpressionNode):

    value: object | None = None