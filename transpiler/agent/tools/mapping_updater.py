import json
import pprint
from pathlib import Path

from transpiler.agent.tools.files import write_file
from transpiler.agent.tools.mapping_analyzer import load_mapping_table
from transpiler.agent.tools.mapping_analyzer import get_unmapped_nodes
from transpiler.agent.tools.node_lookup import get_node
from transpiler.agent.prompts.mapping_prompt import build_mapping_prompt


MAPPING_TABLE_PATH = (
    Path(__file__).resolve().parents[2]
    / "ast"
    / "mapping_table.py"
)


NORMALIZED_NODES = [
    "ModuleNode",
    "ImportNode",
    "ClassNode",
    "FunctionNode",
    "VariableNode",
    "AssignmentNode",
    "ExpressionNode",
    "CallNode",
    "AttributeNode",
    "IfNode",
    "ForNode",
    "WhileNode",
    "WithNode",
    "TryNode",
    "ExceptNode",
    "ReturnNode",
    "RaiseNode",
    "BreakNode",
    "ContinueNode",
    "PassNode",
    "CompareNode",
    "BooleanNode",
    "BinaryOperationNode",
    "UnaryOperationNode",
    "ConditionalExpressionNode",
    "ListNode",
    "TupleNode",
    "DictNode",
    "SetNode",
    "ListComprehensionNode",
    "DictComprehensionNode",
    "SetComprehensionNode",
    "GeneratorNode",
    "IndexNode",
    "SliceNode",
    "LambdaNode",
    "LiteralNode",
]


def generate_mapping_update(
    llm,
    nodes,
):

    response = llm.generate_json(

        build_mapping_prompt(

            mapping_table=load_mapping_table(),

            normalized_nodes=NORMALIZED_NODES,

            nodes=nodes,

        )

    )

    return response

def merge_mapping(mapping, updates):

    for language in updates:

        for category in updates[language]:

            mapping[language][category].update(
                updates[language][category],
            )

    return mapping


def save_mapping(mapping):

    content = (
        "NODE_MAPPING = "
        + pprint.pformat(
            mapping,
            sort_dicts=False,
            width=120,
        )
    )

    write_file(
        MAPPING_TABLE_PATH,
        content,
    )


def update_mapping_table(llm):

    mapping = load_mapping_table()

    unmapped_nodes = get_unmapped_nodes()

    print(
        f"Processing {len(unmapped_nodes)} nodes"
    )

    updates = generate_mapping_update(
        llm,
        unmapped_nodes,
    )

    mapping = merge_mapping(
        mapping,
        updates,
    )

    save_mapping(
        mapping,
    )

    return mapping