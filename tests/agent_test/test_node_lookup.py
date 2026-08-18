from pprint import pprint

from transpiler.agent.tools.node_lookup import (
    get_normalized_node_schema,
)

TEST_NODES = [
    # control flow
    "IfNode",
    "ForNode",
    "TryNode",

    # functions
    "FunctionNode",
    "ParameterNode",

    # operations
    "BinaryOperationNode",
    "CompareNode",
    "BooleanNode",

    # collections
    "ListNode",
    "DictNode",

    # Cython-specific types
    "PointerNode",
    "SimpleTypeNode",

    # imports
    "ImportNode",

    # generators
    "GeneratorNode",

    # classes
    "ClassNode",
]

for node in TEST_NODES:

    print(f"\n{'=' * 80}")
    print(node)
    print('=' * 80)

    pprint(
        get_normalized_node_schema(
            node,
        )
    )