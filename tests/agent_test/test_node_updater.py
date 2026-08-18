from pprint import pprint

from transpiler.agent.prompts.field_prompt import (
    build_field_prompt,
)

from transpiler.agent.prompts.node_prompt import (
    build_node_prompt,
)

from transpiler.agent.tools.node_lookup import (
    get_node_by_normalized_name,
)

from transpiler.agent.tools.nodes_analyzer import (
    analyze_nodes,
)


node_name = "AssertNode"


source_nodes = get_node_by_normalized_name(
    node_name,
)


existing_nodes = analyze_nodes()


print("\nRAW NODE DATA\n")

pprint(
    source_nodes,
)


print("\nFIELD-SELECTION PROMPT\n")

print(

    build_field_prompt(

        node_name=node_name,

        source_nodes=source_nodes,

    )

)


print("\nNODE-GENERATION PROMPT\n")

print(

    build_node_prompt(

        node_name=node_name,

        existing_nodes=existing_nodes,

        schema="<LLM FIELD SELECTION JSON HERE>",

    )

)