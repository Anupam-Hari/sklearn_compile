from pathlib import Path

from transpiler.agent.prompts.field_prompt import (
    build_field_prompt,
)

from transpiler.agent.prompts.node_prompt import (
    build_node_prompt,
)

from transpiler.agent.tools.files import (
    read_file,
    write_file,
)

from transpiler.agent.tools.mapping_analyzer import (
    load_mapping_table,
)

from transpiler.agent.tools.node_lookup import (
    get_node_by_normalized_name,
)

from transpiler.agent.tools.nodes_analyzer import (
    analyze_nodes,
)


NODES_PATH = (
    Path(__file__).resolve().parents[2]
    / "ast"
    / "nodes.py"
)


def get_required_nodes():

    mapping = load_mapping_table()

    required = set()

    for language in mapping.values():

        for category in language.values():

            required.update(
                category.values()
            )

    return required


def get_existing_nodes():

    return set(
        analyze_nodes().keys()
    )


def get_missing_nodes():

    return sorted(
        get_required_nodes()
        - get_existing_nodes()
    )


def generate_node_schema(node_name):

    return build_field_prompt(

        node_name=node_name,

        source_nodes=get_node_by_normalized_name(
            node_name,
        ),

    )


def generate_node(
    node_name,
    schema,
):

    return build_node_prompt(

        node_name=node_name,

        schema=schema,

        existing_nodes=analyze_nodes(),

    )


def append_node(node_code):

    content = read_file(
        NODES_PATH,
    )

    content += (
        "\n\n"
        + node_code
    )

    write_file(
        NODES_PATH,
        content,
    )


def update_nodes():

    return get_missing_nodes()