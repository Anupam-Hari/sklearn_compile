from pathlib import Path

from transpiler.agent.tools.files import read_json


DOCS_DIR = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "node_inventory"
)


INVENTORIES = {

    "python": DOCS_DIR / "python_nodes.json",

    "cython": DOCS_DIR / "cython_nodes.json",

}


def get_all_nodes(language):

    return read_json(

        INVENTORIES[language]

    )


def get_node(language, node_name):

    nodes = get_all_nodes(

        language,

    )

    return nodes.get(

        node_name,

    )


def get_node_attributes(language, node_name):

    node = get_node(

        language,

        node_name,

    )

    if node is None:

        return []

    return node["attributes"]


def get_node_sample(language, node_name):

    node = get_node(

        language,

        node_name,

    )

    if node is None:

        return None

    return node["sample"]


def get_node_example_file(language, node_name):

    node = get_node(

        language,

        node_name,

    )

    if node is None:

        return None

    return node["example_file"]