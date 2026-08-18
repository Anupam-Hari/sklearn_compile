from transpiler.agent.tools.node_updater import (
    generate_node,
    generate_node_schema,
    get_missing_nodes,
)

from transpiler.agent.tools.node_writer import (
    append_node,
)

from transpiler.llm.google import (
    GoogleLLM,
)


llm = GoogleLLM()

missing_nodes = get_missing_nodes()

print(
    f"{len(missing_nodes)} missing nodes found",
)

print(
    missing_nodes,
)


# Don't spend many tokens during the first test.
# Process only the first node.

node_name = missing_nodes[0]

print(
    f"\nProcessing {node_name}\n",
)


# ------------------------------------------------------------------
# LLM call #1: semantic field selection
# ------------------------------------------------------------------

field_prompt = generate_node_schema(
    node_name,
)

field_schema = llm.generate(
    field_prompt,
)

print(
    "\nINTERMEDIATE JSON\n",
)

print(
    field_schema,
)


# ------------------------------------------------------------------
# LLM call #2: node generation
# ------------------------------------------------------------------

node_prompt = generate_node(
    node_name,
    field_schema,
)

node_code = llm.generate(
    node_prompt,
)

print(
    "\nGENERATED NODE\n",
)

print(
    node_code,
)


append_node(
    node_code,
)

print(
    f"\n{node_name} written to nodes.py",
)