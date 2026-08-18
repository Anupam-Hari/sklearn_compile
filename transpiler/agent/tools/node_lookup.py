from pathlib import Path
import re

from transpiler.agent.tools.files import read_json
from transpiler.agent.tools.mapping_analyzer import (
    load_mapping_table,
)

IGNORED_FIELDS = {
    # location metadata
    "lineno",
    "col_offset",
    "end_lineno",
    "end_col_offset",
    "pos",

    # duplicate naming fields
    "class_name",
    "module_name",

    # compiler/internal metadata
    "doc",
    "doc_node",
    "classobj",
    "objstruct_name",
    "typeobj_name",
    "in_pxd",
    "visibility",
    "typedef_flag",
    "check_size",
    "api",
    "dict",
    "target",
    "is_absolute",
    "is_import_as_name",
    "relative_level",
    "reject_duplicates",
    "truedivision",
    "inplace",
    "cascade",
}


FIELD_ALIASES = {
    # operators
    "ops": "operator",
    "op": "operator",

    # operands
    "operand1": "left",
    "operand2": "right",
    "operand": "value",

    # comparisons
    "comparators": "right",

    # imports
    "module_name": "module",
    "imported_names": "names",
    "items": "names",
    "as_name": "alias",

    # collections
    "elts": "elements",
    "args": "elements",
    "key_value_pairs": "items",

    # generators
    "elt": "value",
    "sequence": "iterable",
    "loop": "iterator",

    # functions
    "decorator_list": "decorators",

    # assertions
    "test": "condition",

    # types
    "base_type_node": "base_type",
}

DOCS_DIR = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "node_inventory"
)


INVENTORIES = {
    "python": DOCS_DIR / "python_nodes.json",
    "cython": DOCS_DIR / "cython_nodes.json",
}


def node_type_from_class_name(class_name):

    name = class_name.removesuffix(
        "Node",
    )

    return re.sub(
        r"(?<!^)(?=[A-Z])",
        "_",
        name,
    ).lower()

def get_all_nodes(language):

    return read_json(
        INVENTORIES[language],
    )


def get_node(language, node_name):

    return get_all_nodes(
        language,
    ).get(
        node_name,
    )


def get_normalized_sources(normalized_node):

    mapping = load_mapping_table()

    matches = []

    for language, categories in mapping.items():

        for category, nodes in categories.items():

            for source_node, target_node in nodes.items():

                if target_node == normalized_node:

                    matches.append(
                        {
                            "language": language,
                            "category": category,
                            "source_node": source_node,
                        }
                    )

    return matches


def get_node_by_normalized_name(normalized_node):

    results = []

    for source in get_normalized_sources(
        normalized_node,
    ):

        node = get_node(
            source["language"],
            source["source_node"],
        )

        if node:

            results.append(
                {
                    "language": source["language"],
                    "category": source["category"],
                    "source_node": source["source_node"],
                    "details": node,
                }
            )

    return results


def get_node_attributes(language, node_name):

    node = get_node(
        language,
        node_name,
    )

    return [] if node is None else node["attributes"]


def get_node_sample(language, node_name):

    node = get_node(
        language,
        node_name,
    )

    return None if node is None else node["sample"]


def get_node_example_file(language, node_name):

    node = get_node(
        language,
        node_name,
    )

    return None if node is None else node["example_file"]

def normalize_fields(fields):

    normalized = set()

    for field in fields:

        if field in IGNORED_FIELDS:

            continue

        field = FIELD_ALIASES.get(
            field,
            field,
        )

        normalized.add(
            field,
        )

    return sorted(
        normalized,
    )

def get_normalized_node_schema(normalized_node):

    sources = get_normalized_sources(
        normalized_node,
    )

    fields = set()

    for source in sources:

        node = get_node(
            source["language"],
            source["source_node"],
        )

        if node:

            fields.update(
                node["attributes"],
            )

    return {
        "class_name": normalized_node,
        "node_type": node_type_from_class_name(
            normalized_node,
        ),
        "fields": normalize_fields(
            fields,
        ),
        "source_nodes": sources,
    }