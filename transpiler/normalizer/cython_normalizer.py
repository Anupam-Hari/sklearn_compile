from transpiler.ast.mapping_table import CYTHON_TO_NORMALIZED
from transpiler.ast.unsupported_nodes import UNSUPPORTED_CYTHON_NODES
from transpiler.ast.nodes import (
    CallNode,
    ClassNode,
    EnumNode,
    FunctionNode,
    ImportNode,
    ModuleNode,
    StructNode,
    TypeDefNode,
    VariableNode,
    ExpressionNode,
    ExternNode,
    AssignmentNode,
)

from collections import Counter

UNHANDLED_CYTHON_NODES = Counter()

def get_cython_children(node):

    children = []

    if not hasattr(node, "__dict__"):

        return children

    for value in vars(node).values():

        if hasattr(value, "__dict__"):

            children.append(value)

        elif isinstance(
            value,
            (list, tuple),
        ):

            for item in value:

                if hasattr(item, "__dict__"):

                    children.append(item)

    return children

def _get_name(node):

    for attr in (
        "name",
        "class_name",
        "func_name",
        "cname",
    ):

        value = getattr(node, attr, None)

        if value:
            return value

    declarator = getattr(node, "declarator", None)

    if declarator is not None:

        if hasattr(
            declarator,
            "declared_name",
        ):

            try:

                value = declarator.declared_name()

                if value:
                    return value

            except Exception:
                pass

        value = getattr(
            declarator,
            "name",
            None,
        )

        if value:
            return value

    return "unknown"

def normalize_call(node):

    function = getattr(
        node,
        "function",
        None,
    )

    name = _get_name(
        function,
    )

    return CallNode(
        name=name,
    )

def normalize_import(node):

    node_type = type(node).__name__

    if node_type == "ImportNode":

        names = []

        for item in getattr(node, "items", []):

            if isinstance(item, tuple):

                names.append(item[1])

            else:

                name = _get_name(item)

                if name != "unknown":

                    names.append(name)

        return ImportNode(
            module="",
            names=names,
        )

    module_name = getattr(
        node,
        "module_name",
        "",
    )

    names = []

    for item in getattr(
        node,
        "imported_names",
        [],
    ):

        if isinstance(item, tuple):

            names.append(item[1])

        else:

            names.append(_get_name(item))

    return ImportNode(
        module=module_name,
        names=names,
    )

def normalize_expression(node):

    return ExpressionNode(
        name=_get_name(node),
    )

def normalize_function(node):

    return FunctionNode(
        name=_get_name(node),
    )


def normalize_class(node):

    return ClassNode(
        name=_get_name(node),
        bases=[],
        methods=[],
    )

def normalize_variable(node):

    return VariableNode(
        name=_get_name(node),
    )

def normalize_struct(node):

    return StructNode(
        name=_get_name(node),
    )

def normalize_enum(node):

    return EnumNode(
        name=_get_name(node),
    )

def normalize_assignment(node):

    lhs = getattr(
        node,
        "lhs",
        None,
    )

    name = _get_name(lhs)

    return AssignmentNode(
        name=name,
    )

def normalize_extern(node):

    return ExternNode(
        name=_get_name(node),
    )

def normalize_typedef(node):

    return TypeDefNode(
        name=_get_name(node),
    )


def normalize_node(node):

    node_type = type(node).__name__

    if node_type in UNSUPPORTED_CYTHON_NODES:

        return None

    normalized_type = CYTHON_TO_NORMALIZED.get(
        node_type,
    )

    if normalized_type is None:

        UNHANDLED_CYTHON_NODES[
            node_type
        ] += 1

        return None

    if normalized_type == "ImportNode":

        normalized = normalize_import(node)

    elif normalized_type == "ClassNode":

        normalized = normalize_class(node)

    elif normalized_type == "FunctionNode":

        normalized = normalize_function(node)

    elif normalized_type == "VariableNode":

        normalized = normalize_variable(node)

    elif normalized_type == "StructNode":

        normalized = normalize_struct(node)

    elif normalized_type == "EnumNode":

        normalized = normalize_enum(node)

    elif normalized_type == "TypeDefNode":

        normalized = normalize_typedef(node)

    elif normalized_type == "ExpressionNode":

        normalized = normalize_expression(node)

    elif normalized_type == "ExternNode":

        normalized = normalize_extern(node)

    elif normalized_type == "AssignmentNode":

        normalized = normalize_assignment(node)

    elif normalized_type == "CallNode":

        normalized = normalize_call(node)

    else:

        UNHANDLED_CYTHON_NODES[
            node_type
        ] += 1

        return None

    for child in get_cython_children(node):

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

def normalize_cython_ast(tree):

    module = ModuleNode()

    body = getattr(
        tree,
        "body",
        None,
    )

    stats = getattr(
        body,
        "stats",
        [],
    )

    for node in stats:

        normalized = normalize_node(node)

        if normalized is not None:

            module.add_child(
                normalized,
            )

    return module