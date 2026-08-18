import ast
from pathlib import Path


NODES_PATH = (
    Path(__file__).resolve().parents[2]
    / "ast"
    / "nodes.py"
)


def get_nodes_file():

    return NODES_PATH


def read_nodes_source():

    return NODES_PATH.read_text(
        encoding="utf-8",
    )


def analyze_nodes():

    tree = ast.parse(
        read_nodes_source(),
    )

    nodes = {}

    for node in ast.walk(tree):

        if not isinstance(
            node,
            ast.ClassDef,
        ):
            continue

        bases = []

        for base in node.bases:

            if isinstance(
                base,
                ast.Name,
            ):

                bases.append(
                    base.id,
                )

            elif isinstance(
                base,
                ast.Attribute,
            ):

                bases.append(
                    ast.unparse(base),
                )

        fields = []

        methods = []

        for item in node.body:

            if isinstance(
                item,
                ast.FunctionDef,
            ):

                methods.append(
                    item.name,
                )

                if item.name == "__init__":

                    for statement in ast.walk(item):

                        if not isinstance(
                            statement,
                            ast.Assign,
                        ):
                            continue

                        for target in statement.targets:

                            if not isinstance(
                                target,
                                ast.Attribute,
                            ):
                                continue

                            if not isinstance(
                                target.value,
                                ast.Name,
                            ):
                                continue

                            if target.value.id != "self":
                                continue

                            fields.append(
                                target.attr,
                            )

        nodes[node.name] = {

            "bases": bases,

            "fields": sorted(
                set(fields),
            ),

            "methods": sorted(
                set(methods),
            ),
        }

    return nodes


def get_node(name):

    return analyze_nodes().get(
        name,
    )


def get_node_names():

    return sorted(
        analyze_nodes().keys(),
    )

def get_missing_nodes(mapping_table):

    existing = set(
        analyze_nodes().keys()
    )

    required = set()

    for language in mapping_table.values():

        for category in language.values():

            required.update(
                category.values()
            )

    return sorted(
        required - existing
    )