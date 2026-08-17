import json


def build_mapping_prompt(
    *,
    mapping_table,
    normalized_nodes,
    nodes,
):
    
    return f"""
You are updating an AST mapping table.

Current mapping table:

{json.dumps(mapping_table, indent=4)}

Available normalized nodes:

{json.dumps(normalized_nodes, indent=4)}

Nodes to classify:

{json.dumps(nodes, indent=4)}

Rules:

1. Keep all existing mappings unchanged.

2. Classify every node in the list.

3. Python nodes may belong to:
   - mapped
   - unsupported

4. Cython nodes may belong to:
   - mapped
   - types
   - unsupported

5. Use an existing normalized node whenever possible.

6. Put nodes into "unsupported" only if there is no reasonable mapping.

7. Every input node must appear exactly once in the output.

8. Do not omit any nodes.

9. Return JSON only.

Output format:

{{
    "python": {{
        "mapped": {{}},
        "unsupported": {{}}
    }},
    "cython": {{
        "mapped": {{}},
        "types": {{}},
        "unsupported": {{}}
    }}
}}
"""