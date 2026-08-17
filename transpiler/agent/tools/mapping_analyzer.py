from pathlib import Path

from transpiler.agent.tools.files import read_json


DOCS_DIR = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "node_inventory"
)

PYTHON_NODES = DOCS_DIR / "python_nodes.json"

CYTHON_NODES = DOCS_DIR / "cython_nodes.json"


def load_mapping_table():

    from transpiler.ast.mapping_table import NODE_MAPPING

    return NODE_MAPPING


def get_mapped_nodes():

    mapping = load_mapping_table()

    return {

        "python": {

            **mapping["python"]["mapped"],

            **mapping["python"]["unsupported"],

        },

        "cython": {

            **mapping["cython"]["mapped"],

            **mapping["cython"]["types"],

            **mapping["cython"]["unsupported"],

        },

    }


def analyze_inventory():

    mapped_nodes = get_mapped_nodes()

    report = []

    inventories = [

        ("python", PYTHON_NODES),

        ("cython", CYTHON_NODES),

    ]

    for language, path in inventories:

        nodes = read_json(path)

        language_mappings = mapped_nodes[language]

        for node_name, data in nodes.items():

            report.append(

                {

                    "language": language,

                    "node": node_name,

                    "mapped": node_name in language_mappings,

                    "mapping": language_mappings.get(node_name),

                    "attributes": data["attributes"],

                    "example_file": data["example_file"],

                    "sample": data["sample"],

                }

            )

    return sorted(

        report,

        key=lambda item: (

            item["mapped"],

            item["language"],

            item["node"],

        ),

    )


def get_unmapped_nodes():

    return [

        node

        for node in analyze_inventory()

        if not node["mapped"]

    ]


def get_supported_nodes():

    mapping = load_mapping_table()

    return {

        "python": mapping["python"]["mapped"],

        "cython": mapping["cython"]["mapped"],

    }


def get_unsupported_nodes():

    mapping = load_mapping_table()

    return {

        "python": mapping["python"]["unsupported"],

        "cython": mapping["cython"]["unsupported"],

    }


def get_type_nodes():

    mapping = load_mapping_table()

    return mapping["cython"]["types"]