import ast

from collections import Counter

from transpiler.ast.mapping_table import NODE_MAPPING
from transpiler.ast.nodes import *

PYTHON_TO_NORMALIZED = NODE_MAPPING["python"]["mapped"]

UNHANDLED_PYTHON_NODES = Counter()

NODE_CLASS_MAP = {

    name: globals()[name]

    for name in globals()

    if name.endswith("Node")

}

def get_python_children(node):

    children = []

    for child in ast.iter_child_nodes(node):
        children.append(child)

    return children

def safe_unparse(node):

    if node is None:
        return None

    try:
        return ast.unparse(node)

    except Exception:

        if hasattr(node, "id"):
            return node.id

        if hasattr(node, "name"):
            return node.name

        return str(type(node).__name__)

def normalize_generic(node):

    node_name = getattr(node, "name", None)

    if node_name is None:

        node_name = getattr(
            node,
            "id",
            None,
        )

    return ASTNode(
        node_type="generic",
        name=node_name,
    )

def normalize_parameter(node):

    return ParameterNode(
        name=getattr(node, "arg", None)
        or getattr(node, "name", None),
        annotation=getattr(
            node,
            "annotation",
            None,
        ),
    )

def normalize_arguments(node):

    return ArgumentsNode()

def normalize_assignment(node):

    targets = []

    value = None

    if hasattr(node, "targets"):

        targets = node.targets

    elif hasattr(node, "target"):

        targets = [node.target]

    value = getattr(
        node,
        "value",
        None,
    )

    return AssignmentNode(
        targets=[],
        value=safe_unparse(value)
        if value
        else None,
    )

def normalize_attribute(node):

    return AttributeNode(
        value=safe_unparse(
            getattr(
                node,
                "value",
                None,
            )
        ),
        attribute=getattr(
            node,
            "attr",
            None,
        )
        or getattr(
            node,
            "attribute",
            None,
        ),
    )

def normalize_if(node):

    return IfNode(
        condition=safe_unparse(
            getattr(
                node,
                "test",
                None,
            )
        ),
        body=[],
        orelse=[],
    )

def normalize_for(node):

    return ForNode(
        target=safe_unparse(
            getattr(
                node,
                "target",
                None,
            )
        ),
        iterable=safe_unparse(
            getattr(
                node,
                "iter",
                None,
            )
            or getattr(
                node,
                "iterator",
                None,
            )
        ),
        body=[],
    )

def normalize_while(node):

    return WhileNode(
        condition=safe_unparse(
            getattr(
                node,
                "test",
                None,
            )
        ),
        body=[],
    )

def normalize_with(node):

    return WithNode(
        items=[],
        body=[],
    )

def normalize_try(node):

    return TryNode(
        body=[],
        handlers=[],
        finalbody=[],
    )

def normalize_except(node):

    return ExceptNode(
        exception_type=safe_unparse(
            getattr(
                node,
                "type",
                None,
            )
        ),
        body=[],
    )

def normalize_return(node):

    return ReturnNode(
        attributes={
            "value": safe_unparse(
                getattr(
                    node,
                    "value",
                    None,
                )
            )
        }
    )

def normalize_yield(node):

    return YieldNode(
        attributes={
            "value": safe_unparse(
                getattr(
                    node,
                    "value",
                    None,
                )
            )
        }
    )

def normalize_compare(node):

    return CompareNode(
        left=safe_unparse(
            getattr(
                node,
                "left",
                None,
            )
        ),
        operator=type(
            getattr(
                node,
                "ops",
                [None],
            )[0]
        ).__name__
        if getattr(
            node,
            "ops",
            None,
        )
        else None,
    )

def normalize_boolean(node):

    return BooleanNode(
        operator=type(
            getattr(
                node,
                "op",
                None,
            )
        ).__name__
        if getattr(
            node,
            "op",
            None,
        )
        else None,
    )

def normalize_binary_operation(node):

    return BinaryOperationNode(
        left=safe_unparse(
            getattr(
                node,
                "left",
                None,
            )
        ),
        operator=type(
            getattr(
                node,
                "op",
                None,
            )
        ).__name__
        if getattr(
            node,
            "op",
            None,
        )
        else None,
        right=safe_unparse(
            getattr(
                node,
                "right",
                None,
            )
        ),
    )

def normalize_unary_operation(node):

    return UnaryOperationNode(
        operator=type(
            getattr(
                node,
                "op",
                None,
            )
        ).__name__
        if getattr(
            node,
            "op",
            None,
        )
        else None,
        operand=safe_unparse(
            getattr(
                node,
                "operand",
                None,
            )
        ),
    )

def normalize_conditional_expression(node):

    return ConditionalExpressionNode()

def normalize_collection(node):

    values = getattr(
        node,
        "elts",
        [],
    )

    return type(node)

def normalize_list(node):

    return ListNode()

def normalize_tuple(node):

    return TupleNode()

def normalize_dict(node):

    return DictNode()

def normalize_set(node):

    return SetNode()

def normalize_comprehension(node):

    return ComprehensionNode()

def normalize_generator(node):

    return GeneratorNode()

def normalize_index(node):

    return IndexNode()

def normalize_slice(node):

    return SliceNode()

def normalize_literal(node):

    return LiteralNode(
        value=getattr(
            node,
            "value",
            None,
        ),
    )

def normalize_formatted_value(node):

    return FormattedValueNode()

def normalize_fstring(node):

    return FStringNode()

def normalize_delete(node):

    return DeleteNode()

def normalize_struct(node):

    return StructNode(
        name=safe_unparse(node),
    )

def normalize_enum(node):

    return EnumNode(
        name=safe_unparse(node),
    )

def normalize_typedef(node):

    return TypeDefNode(
        name=safe_unparse(node),
    )

def normalize_extern(node):

    return ExternNode(
        name=safe_unparse(node),
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
        names=[alias.name for alias in node.names],
        level=node.level,
    )

def normalize_call(node):

    if isinstance(node, ast.Call):

        return CallNode(
            function=safe_unparse(node.func),
            arguments=[
                safe_unparse(arg)
                for arg in node.args
            ],
        )

    return CallNode(
        function=safe_unparse(
            getattr(
                node,
                "function",
                None,
            )
        ),
    )

def normalize_expression(node):

    return ExpressionNode(
        value=safe_unparse(node),
    )

def normalize_function(node):

    if isinstance(node, ast.Lambda):

        return LambdaNode(
            parameters=[],
        )

    return FunctionNode(
        name=node.name,
        parameters=[],
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

    normalized_name = PYTHON_TO_NORMALIZED.get(node_type)

    if normalized_name is None:

        UNHANDLED_PYTHON_NODES[node_type] += 1

        return None

    normalizer = NORMALIZER_FUNCTIONS.get(
        normalized_name,
        normalize_generic,
    )

    normalized = normalizer(node)

    if normalized is None:
        return None

    for child in get_python_children(node):

        normalized_child = normalize_node(child)

        if normalized_child is not None:

            normalized.children.append(
                normalized_child,
            )

            if (
                isinstance(normalized, ClassNode)
                and isinstance(normalized_child, FunctionNode)
            ):

                normalized.methods.append(
                    normalized_child,
                )

    return normalized

def normalize_python_ast(tree):

    module = ModuleNode()

    for node in tree.body:

        normalized = normalize_node(node)

        if normalized is not None:

            module.children.append(
                normalized,
            )

    return module

NORMALIZER_FUNCTIONS = {

    "ImportNode": normalize_import,
    "ImportAliasNode": normalize_generic,

    "ParameterNode": normalize_parameter,
    "ArgumentsNode": normalize_arguments,

    "FunctionNode": normalize_function,
    "LambdaNode": normalize_function,

    "ClassNode": normalize_class,

    "VariableNode": normalize_variable,
    "AssignmentNode": normalize_assignment,

    "ExpressionNode": normalize_expression,
    "AttributeNode": normalize_attribute,
    "CallNode": normalize_call,
    "CastNode": normalize_generic,

    "IfNode": normalize_if,
    "ForNode": normalize_for,
    "WhileNode": normalize_while,
    "WithNode": normalize_with,
    "TryNode": normalize_try,

    "ExceptNode": normalize_except,
    "RaiseNode": normalize_generic,
    "AssertNode": normalize_generic,

    "ReturnNode": normalize_return,
    "YieldNode": normalize_yield,
    "YieldFromNode": normalize_yield,

    "BreakNode": normalize_generic,
    "ContinueNode": normalize_generic,
    "PassNode": normalize_generic,

    "CompareNode": normalize_compare,
    "BooleanNode": normalize_boolean,
    "BinaryOperationNode": normalize_binary_operation,
    "UnaryOperationNode": normalize_unary_operation,
    "ConditionalExpressionNode": normalize_conditional_expression,

    "ListNode": normalize_list,
    "TupleNode": normalize_tuple,
    "DictNode": normalize_dict,
    "SetNode": normalize_set,

    "ComprehensionNode": normalize_comprehension,
    "ListComprehensionNode": normalize_comprehension,
    "DictComprehensionNode": normalize_comprehension,
    "SetComprehensionNode": normalize_comprehension,

    "GeneratorNode": normalize_generator,

    "IndexNode": normalize_index,
    "SliceNode": normalize_slice,

    "LiteralNode": normalize_literal,
    "FormattedValueNode": normalize_formatted_value,
    "FStringNode": normalize_fstring,
    "FormattedStringNode": normalize_fstring,

    "DeleteNode": normalize_delete,

    "StructNode": normalize_struct,
    "EnumNode": normalize_enum,
    "TypeDefNode": normalize_typedef,
    "ExternNode": normalize_extern,
}
