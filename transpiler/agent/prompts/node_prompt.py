import json


def build_node_prompt(
    *,
    node_name,
    schema,
    existing_nodes,
):

    return f"""
You are updating nodes.py for an AST transpiler.

Normalized node to generate:

{node_name}

Existing nodes in nodes.py:

{json.dumps(existing_nodes, indent=4)}

Normalized node schema:

{json.dumps(schema, indent=4)}

Rules:

1. Generate exactly one class.

2. Return Python code only.

3. Follow the coding style used by the existing nodes.

4. Inherit from ASTNode.

5. Use @dataclass.

6. Preserve the node_type provided in the schema.

7. Use only the constructor_parameters defined in the schema.

8. Do not invent additional fields.

9. Constructor parameters must be explicit.

10. Store only the fields listed in "attributes" inside the attributes dictionary.

11. Store only the fields listed in "children" inside the children list.

12. Build the children list explicitly.

Example:

children = []

if left is not None:

    children.append(left)

if right is not None:

    children.append(right)

13. Do not pass dictionaries into children.

14. Do not create self.field assignments unless an existing node uses the same pattern.

15. Keep constructors as simple as possible.

16. Do not add methods other than __init__.

17. Do not modify any existing classes.

Example input schema:

{{
    "node_type": "binary_operation",
    "constructor_parameters": [
        "operator",
        "left",
        "right"
    ],
    "attributes": [
        "operator"
    ],
    "children": [
        "left",
        "right"
    ]
}}

Example output:

@dataclass
class BinaryOperationNode(ASTNode):

    def __init__(
        self,
        operator=None,
        left=None,
        right=None,
    ):

        children = []

        if left is not None:

            children.append(left)

        if right is not None:

            children.append(right)

        super().__init__(
            node_type="binary_operation",
            attributes={{
                "operator": operator,
            }},
            children=children,
        )

Return only the class definition.
"""