import ast

from transpiler.ast.mapping_table import PYTHON_TO_NORMALIZED
from transpiler.ast.nodes import (
    ClassNode,
    ConstantNode,
    EnumNode,
    FunctionNode,
    ImportNode,
    ModuleNode,
    StructNode,
    TypeDefNode,
    VariableNode,
    ExpressionNode,
)
from collections import Counter

UNHANDLED_PYTHON_NODES = Counter()

def get_python_children(node):

    return list(
        ast.iter_child_nodes(node)
    )

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

def normalize_expression(node):

    try:

        name = ast.unparse(node)

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
        methods=[],
    )

def normalize_variable(node):

    return VariableNode(
        name=node.id,
    )

def normalize_constant(node):

    value = getattr(
        node,
        "value",
        None,
    )

    return ConstantNode(
        name=str(value),
        value=value,
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

    elif normalized_type == "VariableNode":

        normalized = normalize_variable(node)

    elif normalized_type == "AssignmentNode":

        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    name = target.id

                    if name.isupper():

                        normalized = ConstantNode(
                            name=name,
                            value=ast.unparse(
                                node.value,
                            ),
                        )

                    else:

                        normalized = VariableNode(
                            name=name,
                        )

                    break

        elif isinstance(node, ast.AnnAssign):

            if isinstance(node.target, ast.Name):

                name = node.target.id

                if name.isupper():

                    normalized = ConstantNode(
                        name=name,
                        value=(
                            ast.unparse(node.value)
                            if node.value
                            else None
                        ),
                    )

                else:

                    normalized = VariableNode(
                        name=name,
                    )

    elif normalized_type == "ExpressionNode":

        normalized = normalize_expression(node)

    else:

        UNHANDLED_PYTHON_NODES[
            node_type
        ] += 1

        return None

    if normalized is None:

        return None

    for child in get_python_children(node):

        normalized_child = normalize_node(
            child,
        )

        if normalized_child is not None:

            normalized.children.append(
                normalized_child,
            )

            if (
                normalized.node_type == "class"
                and normalized_child.node_type == "function"
            ):

                normalized.methods.append(
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

            module.add_child(
                normalized,
            )

    return module