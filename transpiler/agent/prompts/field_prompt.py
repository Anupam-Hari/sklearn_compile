import json


def build_field_prompt(
    *,
    node_name,
    source_nodes,
):

    return f"""
You are designing a normalized AST node for a transpiler.

Normalized node:

{node_name}

Source AST nodes:

{json.dumps(source_nodes, indent=4)}

Your task is to determine which fields should be preserved in the normalized node.

Rules:

1. Ignore source-language implementation details.

2. Ignore parser metadata.

3. Ignore compiler metadata.

4. Ignore source locations such as:
   - lineno
   - col_offset
   - end_lineno
   - end_col_offset
   - pos

5. Merge duplicate fields whenever they represent the same concept.

6. Rename fields when multiple source nodes use different names for the same concept.

7. Keep only fields that preserve AST semantics.

8. Separate primitive values from nested AST nodes.

9. Constructor parameters should contain only the essential semantic fields.

10. Nested AST nodes should become children.

11. Primitive values should become attributes.

12. The normalized node must work for both Python and Cython.

Return JSON only.

Output format:

{{
    "node_type": "",

    "constructor_parameters": [],

    "attributes": [],

    "children": [],

    "notes": ""
}}
"""