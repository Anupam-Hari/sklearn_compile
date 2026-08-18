import ast

from transpiler.ast.mapping_table import PYTHON_TO_NORMALIZED
from transpiler.ast.nodes import *
from collections import Counter

UNHANDLED_PYTHON_NODES = Counter()

def get_python_children(node):

    children = []

    if isinstance(node, ast.Module):

        children.extend(node.body)

    elif isinstance(node, ast.ClassDef):

        children.extend(node.body)

    elif isinstance(node, ast.FunctionDef):

        children.extend(node.body)

    elif isinstance(node, ast.If):

        children.extend(node.body)
        children.extend(node.orelse)

    elif isinstance(node, ast.For):

        children.extend(node.body)
        children.extend(node.orelse)

    elif isinstance(node, ast.While):

        children.extend(node.body)
        children.extend(node.orelse)

    elif isinstance(node, ast.With):

        children.extend(node.body)

    elif isinstance(node, ast.Try):

        children.extend(node.body)
        children.extend(node.handlers)
        children.extend(node.orelse)
        children.extend(node.finalbody)

    elif isinstance(node, ast.ExceptHandler):

        children.extend(node.body)

    elif isinstance(node, ast.Expr):

        children.append(node.value)

    return children

def normalize_import(node):

    if isinstance(node, ast.Import):

        return ImportNode(
            module="",
            names=[
                alias.name
                for alias in node.names
            ],
        )

    return ImportNode(
        module=node.module or "",
        names=[
            alias.name
            for alias in node.names
        ],
    )

def normalize_call(node):

    try:

        name = ast.unparse(
            node.func,
        )

    except Exception:

        name = "unknown"

    arguments = []

    for argument in node.args:

        normalized = normalize_node(
            argument,
        )

        if normalized is not None:

            arguments.append(
                normalized,
            )

    return CallNode(
        name=name,
        arguments=arguments,
    )

def normalize_return(node):

    value = None

    if node.value is not None:

        value = normalize_node(
            node.value,
        )

    return ReturnNode(
        value=value,
    )

def normalize_binary_operation(node):

    operator = type(
        node.op,
    ).__name__

    left = normalize_node(
        node.left,
    )

    right = normalize_node(
        node.right,
    )

    return BinaryOperationNode(
        operator=operator,
        left=left,
        right=right,
    )

def normalize_expression(node):

    try:

        name = ast.unparse(
            node,
        )

    except Exception:

        name = "expression"

    return ExpressionNode(
        name=name,
    )

def normalize_function(node):

    return FunctionNode(
        name=node.name,
    )

def normalize_class(node):

    bases = []

    for base in node.bases:

        try:

            bases.append(
                ast.unparse(base)
            )

        except Exception:

            pass

    return ClassNode(
        name=node.name,
        bases=bases,
    )

def normalize_literal(node):

    return LiteralNode(
        value=getattr(
            node,
            "value",
            None,
        ),
    )

def normalize_assignment(node):

    target = None

    if isinstance(node, ast.Assign):

        if node.targets:

            try:

                target = ast.unparse(
                    node.targets[0],
                )

            except Exception:

                pass

    elif isinstance(node, ast.AnnAssign):

        try:

            target = ast.unparse(
                node.target,
            )

        except Exception:

            pass

    elif isinstance(node, ast.AugAssign):

        try:

            target = ast.unparse(
                node.target,
            )

        except Exception:

            pass

    value = None
    if node.value is not None:

        value = normalize_node(
            node.value,
        )

    return AssignmentNode(
        target=target,
        value=value,
    )

def normalize_variable(node):

    return VariableNode(
        name=node.id,
    )

def normalize_literal(node):

    return LiteralNode(
        value=getattr(
            node,
            "value",
            None,
        ),
    )
def normalize_struct(node):

    return StructNode(
        name=node.name,
    )

def normalize_enum(node):

    return EnumNode(
        name=node.name,
    )

def normalize_typedef(node):

    return TypeDefNode(
        name=node.name,
    )

def normalize_node(node):

    node_type = type(node).__name__
    print(
        node_type,
        PYTHON_TO_NORMALIZED.get(
            node_type,
        ),
    )

    normalized_type = PYTHON_TO_NORMALIZED.get(
        node_type,
    )

    normalized = None

    if normalized_type == "ImportNode":

        normalized = normalize_import(node)

    elif normalized_type == "ClassNode":

        normalized = normalize_class(node)

    elif normalized_type == "FunctionNode":

        normalized = normalize_function(node)

    elif normalized_type == "AssignmentNode":

        normalized = normalize_assignment(node)

    elif normalized_type == "CallNode":

        normalized = normalize_call(node)

    elif normalized_type == "ExpressionNode":

        normalized = normalize_expression(node)

    elif normalized_type == "AttributeNode":

        normalized = AttributeNode()

    elif normalized_type == "IfNode":

        normalized = IfNode()

    elif normalized_type == "ForNode":

        normalized = ForNode()

    elif normalized_type == "WhileNode":

        normalized = WhileNode()

    elif normalized_type == "WithNode":

        normalized = WithNode()

    elif normalized_type == "TryNode":

        normalized = TryNode()

    elif normalized_type == "ExceptNode":

        normalized = ExceptNode()

    elif normalized_type == "ReturnNode":

        normalized = normalize_return(node)

    elif normalized_type == "RaiseNode":

        normalized = RaiseNode()

    elif normalized_type == "BreakNode":

        normalized = BreakNode()

    elif normalized_type == "ContinueNode":

        normalized = ContinueNode()

    elif normalized_type == "PassNode":

        normalized = PassNode()

    elif normalized_type == "CompareNode":

        normalized = CompareNode()

    elif normalized_type == "BooleanNode":

        normalized = BooleanNode()

    elif normalized_type == "BinaryOperationNode":

        normalized = normalize_binary_operation(node)

    elif normalized_type == "UnaryOperationNode":

        normalized = UnaryOperationNode()

    elif normalized_type == "ListNode":

        normalized = ListNode()

    elif normalized_type == "TupleNode":

        normalized = TupleNode()

    elif normalized_type == "DictNode":

        normalized = DictNode()

    elif normalized_type == "SetNode":

        normalized = SetNode()

    elif normalized_type == "IndexNode":

        normalized = SliceNode()

    elif normalized_type == "SliceNode":

        normalized = SliceNode()

    elif isinstance(node, ast.Constant):

        normalized = normalize_literal(node)

    elif isinstance(node, ast.Name):

        normalized = normalize_variable(node)

    else:

        UNHANDLED_PYTHON_NODES[
            node_type
        ] += 1

        return None

    for child in get_python_children(
        node,
    ):

        normalized_child = normalize_node(
            child,
        )

        if isinstance(
            normalized,
            ReturnNode,
        ):

            return normalized

        if isinstance(
            normalized,
            (
                ReturnNode,
                BinaryOperationNode,
            ),
        ):

            return normalized

        if isinstance(
            normalized,
            (
                ReturnNode,
                BinaryOperationNode,
                AssignmentNode,
                CallNode,
            ),
        ):

            return normalized

        if normalized_child is not None:

            normalized.children.append(
                normalized_child,
            )

    return normalized

def normalize_python_ast(tree):

    module = ModuleNode()

    for node in tree.body:

        normalized = normalize_node(
            node,
        )

        if normalized is not None:

            module.children.append(
                normalized,
            )

    return module