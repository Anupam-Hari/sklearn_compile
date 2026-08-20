from __future__ import annotations

from dataclasses import dataclass, field


# =============================================================================
# Base node
# =============================================================================

@dataclass
class ASTNode:

    children: list["ASTNode"] = field(
        default_factory=list,
    )


class TypedNode(ASTNode):

    NODE_TYPE = "node"

    def __init__(
        self,
        name=None,
        attributes=None,
        children=None,
    ):
        super().__init__(
            node_type=self.NODE_TYPE,
            name=name,
            attributes=attributes or {},
            children=children or [],
        )


# =============================================================================
# Module
# =============================================================================

class ModuleNode(TypedNode):

    NODE_TYPE = "module"

    def __init__(
        self,
        name=None,
        functions=None,
        classes=None,
        imports=None,
        attributes=None,
        children=None,
    ):
        super().__init__(name, attributes, children)

        self.functions = functions or []
        self.classes = classes or []
        self.imports = imports or []

        self.children.extend(self.imports)
        self.children.extend(self.classes)
        self.children.extend(self.functions)


# =============================================================================
# Imports
# =============================================================================

class ImportNode(TypedNode):

    NODE_TYPE = "import"

    def __init__(
        self,
        module="",
        names=None,
        level=0,
        attributes=None,
        children=None,
    ):
        super().__init__(module, attributes, children)

        self.module = module
        self.names = names or []
        self.level = level

    pass

class ImportAliasNode(TypedNode):

    NODE_TYPE = "import_alias"

    def __init__(
        self,
        name,
        alias=None,
        attributes=None,
        children=None,
    ):
        super().__init__(name, attributes, children)

        self.alias = alias


# =============================================================================
# Functions
# =============================================================================

class ParameterNode(TypedNode):

    NODE_TYPE = "parameter"

    def __init__(
        self,
        name,
        annotation=None,
        default=None,
        attributes=None,
        children=None,
    ):
        super().__init__(name, attributes, children)

        self.annotation = annotation
        self.default = default


class ArgumentsNode(TypedNode):

    NODE_TYPE = "arguments"

    def __init__(
        self,
        parameters=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.parameters = parameters or []
        self.children.extend(self.parameters)


class FunctionNode(TypedNode):

    NODE_TYPE = "function"

    def __init__(
        self,
        name,
        parameters=None,
        returns=None,
        decorators=None,
        body=None,
        attributes=None,
        children=None,
    ):
        super().__init__(name, attributes, children)

        self.parameters = parameters or []
        self.decorators = decorators or []
        self.returns = returns
        self.body = body or []

        self.children.extend(self.parameters)
        self.children.extend(self.body)


class LambdaNode(TypedNode):

    NODE_TYPE = "lambda"

    def __init__(
        self,
        parameters=None,
        body=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.parameters = parameters or []
        self.body = body


# =============================================================================
# Classes
# =============================================================================

class ClassNode(TypedNode):

    NODE_TYPE = "class"

    def __init__(
        self,
        name,
        bases=None,
        methods=None,
        attributes=None,
        children=None,
    ):
        super().__init__(name, attributes, children)

        self.bases = bases or []
        self.methods = methods or []

        self.children.extend(self.methods)


# =============================================================================
# Variables and assignments
# =============================================================================

class VariableNode(TypedNode):

    NODE_TYPE = "variable"

    def __init__(
        self,
        name,
        scope=None,
        value=None,
        attributes=None,
        children=None,
    ):
        super().__init__(name, attributes, children)

        self.scope = scope
        self.value = value


class AssignmentNode(TypedNode):

    NODE_TYPE = "assignment"

    def __init__(
        self,
        targets=None,
        value=None,
        operator="=",
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.targets = targets or []
        self.value = value
        self.operator = operator


# =============================================================================
# Expressions
# =============================================================================

class ExpressionNode(TypedNode):

    NODE_TYPE = "expression"

    def __init__(
        self,
        value=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.value = value


class AttributeNode(TypedNode):

    NODE_TYPE = "attribute"

    def __init__(
        self,
        value=None,
        attribute=None,
        attributes=None,
        children=None,
    ):
        super().__init__(attribute, attributes, children)

        self.value = value
        self.attribute = attribute


class CastNode(TypedNode):

    NODE_TYPE = "cast"

    def __init__(
        self,
        target_type=None,
        value=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.target_type = target_type
        self.value = value

        if value:
            self.children.append(value)


class CallNode(TypedNode):

    NODE_TYPE = "call"
    def __init__(
        self,
        function=None,
        arguments=None,
        keywords=None,
        attributes=None,
        children=None,
    ):
        super().__init__(
            None,
            attributes,
            children,
        )
        self.function = function
        self.arguments = arguments or []
        self.keywords = keywords or []


class KeywordArgumentNode(TypedNode):

    NODE_TYPE = "keyword_argument"

    def __init__(
        self,
        name,
        value=None,
        attributes=None,
        children=None,
    ):
        super().__init__(name, attributes, children)

        self.value = value

        if value:
            self.children.append(value)


# =============================================================================
# Control flow
# =============================================================================

class IfNode(TypedNode):

    NODE_TYPE = "if"

    def __init__(
        self,
        condition=None,
        body=None,
        orelse=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.condition = condition
        self.body = body or []
        self.orelse = orelse or []

        if condition:
            self.children.append(condition)

        self.children.extend(self.body)
        self.children.extend(self.orelse)


class ForNode(TypedNode):

    NODE_TYPE = "for"

    def __init__(
        self,
        target=None,
        iterable=None,
        body=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.target = target
        self.iterable = iterable
        self.body = body or []

        if target:
            self.children.append(target)

        if iterable:
            self.children.append(iterable)

        self.children.extend(self.body)


class WhileNode(TypedNode):

    NODE_TYPE = "while"

    def __init__(
        self,
        condition=None,
        body=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.condition = condition
        self.body = body or []

        if condition:
            self.children.append(condition)

        self.children.extend(self.body)


class WithNode(TypedNode):

    NODE_TYPE = "with"

    def __init__(
        self,
        items=None,
        body=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.items = items or []
        self.body = body or []

        self.children.extend(self.items)
        self.children.extend(self.body)


class WithItemNode(TypedNode):

    NODE_TYPE = "with_item"

    def __init__(
        self,
        context=None,
        alias=None,
        attributes=None,
        children=None,
    ):
        super().__init__(alias, attributes, children)

        self.context = context
        self.alias = alias

        if context:
            self.children.append(context)


class TryNode(TypedNode):

    NODE_TYPE = "try"

    def __init__(
        self,
        body=None,
        handlers=None,
        finalbody=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.body = body or []
        self.handlers = handlers or []
        self.finalbody = finalbody or []

        self.children.extend(self.body)
        self.children.extend(self.handlers)
        self.children.extend(self.finalbody)

# =============================================================================
# Exceptions
# =============================================================================

class ExceptNode(TypedNode):

    NODE_TYPE = "except"

    def __init__(
        self,
        exception_type=None,
        body=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.exception_type = exception_type
        self.body = body or []

        self.children.extend(self.body)


class RaiseNode(TypedNode):

    NODE_TYPE = "raise"

    def __init__(
        self,
        exception=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.exception = exception

        if exception:
            self.children.append(exception)


class AssertNode(TypedNode):
    NODE_TYPE = "assert"


# =============================================================================
# Return / yield
# =============================================================================

class ReturnNode(TypedNode):
    NODE_TYPE = "return"


class YieldNode(TypedNode):
    NODE_TYPE = "yield"


class YieldFromNode(TypedNode):
    NODE_TYPE = "yield_from"


# =============================================================================
# Loop control
# =============================================================================

class BreakNode(TypedNode):
    NODE_TYPE = "break"


class ContinueNode(TypedNode):
    NODE_TYPE = "continue"


class PassNode(TypedNode):
    NODE_TYPE = "pass"


# =============================================================================
# Operators
# =============================================================================

class CompareNode(TypedNode):

    NODE_TYPE = "compare"

    def __init__(
        self,
        left=None,
        operator=None,
        right=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.left = left
        self.operator = operator
        self.right = right

        if left:
            self.children.append(left)

        if right:
            self.children.append(right)


class BooleanNode(TypedNode):

    NODE_TYPE = "boolean"

    def __init__(
        self,
        operator=None,
        operands=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.operator = operator
        self.operands = operands or []

        self.children.extend(self.operands)


class BinaryOperationNode(TypedNode):

    NODE_TYPE = "binary_operation"

    def __init__(
        self,
        left=None,
        operator=None,
        right=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.left = left
        self.operator = operator
        self.right = right

        if left:
            self.children.append(left)

        if right:
            self.children.append(right)


class UnaryOperationNode(TypedNode):

    NODE_TYPE = "unary_operation"

    def __init__(
        self,
        operator=None,
        operand=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.operator = operator
        self.operand = operand

        if operand:
            self.children.append(operand)


class ConditionalExpressionNode(TypedNode):
    NODE_TYPE = "conditional_expression"


# =============================================================================
# Collections
# =============================================================================

class ListNode(TypedNode):
    NODE_TYPE = "list"


class TupleNode(TypedNode):
    NODE_TYPE = "tuple"


class DictNode(TypedNode):
    NODE_TYPE = "dict"


class SetNode(TypedNode):
    NODE_TYPE = "set"


class DictItemNode(TypedNode):
    NODE_TYPE = "dict_item"


# =============================================================================
# Comprehensions
# =============================================================================

class ComprehensionNode(TypedNode):
    NODE_TYPE = "comprehension"


class ListComprehensionNode(TypedNode):
    NODE_TYPE = "list_comprehension"


class DictComprehensionNode(TypedNode):
    NODE_TYPE = "dict_comprehension"


class SetComprehensionNode(TypedNode):
    NODE_TYPE = "set_comprehension"


class GeneratorNode(TypedNode):
    NODE_TYPE = "generator"


# =============================================================================
# Indexing
# =============================================================================

class IndexNode(TypedNode):
    NODE_TYPE = "index"


class SliceNode(TypedNode):
    NODE_TYPE = "slice"


# =============================================================================
# Literals
# =============================================================================

class LiteralNode(TypedNode):

    NODE_TYPE = "literal"

    def __init__(
        self,
        value=None,
        attributes=None,
        children=None,
    ):
        super().__init__(None, attributes, children)

        self.value = value


class FormattedValueNode(TypedNode):
    NODE_TYPE = "formatted_value"


class FStringNode(TypedNode):
    NODE_TYPE = "f_string"


class FormattedStringNode(TypedNode):
    NODE_TYPE = "formatted_string"


# =============================================================================
# Misc
# =============================================================================

class DeleteNode(TypedNode):
    NODE_TYPE = "delete"


class ArrayNode(TypedNode):
    NODE_TYPE = "array"


# =============================================================================
# C declarations
# =============================================================================

class StructNode(TypedNode):
    NODE_TYPE = "struct"


class EnumNode(TypedNode):
    NODE_TYPE = "enum"


class EnumValueNode(TypedNode):
    NODE_TYPE = "enum_value"


class TypeDefNode(TypedNode):
    NODE_TYPE = "typedef"


class ExternNode(TypedNode):
    NODE_TYPE = "extern"


# =============================================================================
# Declarators
# =============================================================================

class FunctionDeclaratorNode(TypedNode):
    NODE_TYPE = "function_declarator"


class VariableDeclaratorNode(TypedNode):
    NODE_TYPE = "variable_declarator"


class PointerNode(TypedNode):
    NODE_TYPE = "pointer"


class ArrayDeclaratorNode(TypedNode):
    NODE_TYPE = "array_declarator"


class ReferenceNode(TypedNode):
    NODE_TYPE = "reference"


# =============================================================================
# C types
# =============================================================================

class SimpleTypeNode(TypedNode):
    NODE_TYPE = "simple_type"


class ComplexTypeNode(TypedNode):
    NODE_TYPE = "complex_type"


class QualifiedTypeNode(TypedNode):
    NODE_TYPE = "qualified_type"


class NestedTypeNode(TypedNode):
    NODE_TYPE = "nested_type"


class TupleTypeNode(TypedNode):
    NODE_TYPE = "tuple_type"


class FusedTypeNode(TypedNode):
    NODE_TYPE = "fused_type"


class MemoryViewTypeNode(TypedNode):
    NODE_TYPE = "memory_view_type"


class TemplatedTypeNode(TypedNode):
    NODE_TYPE = "templated_type"


# =============================================================================
# sizeof
# =============================================================================

class SizeofTypeNode(TypedNode):
    NODE_TYPE = "sizeof_type"


class SizeofVariableNode(TypedNode):
    NODE_TYPE = "sizeof_variable"