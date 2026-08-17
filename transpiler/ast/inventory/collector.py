import json
import ast

from collections import defaultdict
from logging import root
from pathlib import Path

from transpiler.parser.python_parser import parse_python_file
from transpiler.parser.cython_parser import parse_cython_file


OUTPUT_DIR = Path("node_inventory")

def get_cython_children(node):

    children = []

    for attr in getattr(node, "child_attrs", ()):

        value = getattr(node, attr, None)

        if value is None:

            continue

        if isinstance(value, list):

            children.extend(value)

        else:

            children.append(value)

    return children


def get_python_children(node):

    return ast.iter_child_nodes(node)


def walk_ast(node, inventory, file_path, visited, get_children):

    if node is None:

        return

    node_id = id(node)

    if node_id in visited:

        return

    visited.add(node_id)

    node_type = type(node).__name__

    try:

        attributes = sorted(vars(node).keys())

    except TypeError:

        attributes = []

    entry = inventory[node_type]

    entry["count"] += 1

    entry["attributes"].update(attributes)

    entry["files"].add(str(file_path))

    if entry["sample"] is None:

        entry["sample"] = serialize_node(node)

    for child in get_children(node):

        walk_ast(child, inventory, file_path, visited, get_children)


def create_inventory():

    return defaultdict(

        lambda: {

            "count": 0,

            "attributes": set(),

            "files": set(),

            "sample": None,

        }

    )


def collect_language_nodes(root, suffixes, parser, get_children):

    inventory = create_inventory()

    failed = []

    for path in root.rglob("*"):

        if path.suffix not in suffixes:

            continue

        if "tests" in path.parts:

            continue

        try:

            tree = parser(path)

            walk_ast(
                tree,
                inventory,
                path,
                set(),
                get_children,
            )

        except Exception as e:

            failed.append(
                (
                    str(path),
                    type(e).__name__,
                    str(e),
                )
            )

    return inventory, failed


def serialize(inventory):

    output = {}

    for node_name, data in sorted(inventory.items()):

        output[node_name] = {

            "count": data["count"],

            "attributes": sorted(
                data["attributes"]
            ),

            "example_file": sorted(
                data["files"]
            )[0],

            "files": sorted(
                data["files"]
            )[:10],

            "sample": data["sample"],

        }

    return output

def serialize_failed(failed):

    return [

        {
            "file": file,
            "exception": exception,
            "message": message,
        }

        for file, exception, message in failed

    ]

def serialize_node(node, depth=0, visited=None):

    if visited is None:

        visited = set()

    if node is None:

        return None

    if depth > 3:

        return type(node).__name__

    node_id = id(node)

    if node_id in visited:

        return "<recursive>"

    visited.add(node_id)

    if isinstance(node, (str, int, float, bool)):

        return node

    if isinstance(node, list):

        return [

            serialize_node(
                item,
                depth + 1,
                visited,
            )

            for item in node[:10]

        ]

    try:

        attributes = vars(node)

    except TypeError:

        return repr(node)

    output = {

        "__type__": type(node).__name__,

    }

    for key, value in attributes.items():

        if key.startswith("_"):

            continue

        if isinstance(
            value,
            (str, int, float, bool),
        ):

            output[key] = value

        elif isinstance(
            value,
            list,
        ):

            output[key] = [

                serialize_node(
                    item,
                    depth + 1,
                    visited,
                )

                for item in value[:10]

            ]

        elif hasattr(
            value,
            "__dict__",
        ):

            output[key] = serialize_node(
                value,
                depth + 1,
                visited,
            )

    return output

def load_mapping_table():

    try:

        from transpiler.ast.mapping_table import (
            NODE_MAPPING,
        )

        return set(NODE_MAPPING)

    except Exception:

        return set()


def find_unknown_nodes(inventory, known_nodes):

    return {

        node: data

        for node, data in inventory.items()

        if node not in known_nodes

    }


def write_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(

        json.dumps(
            data,
            indent=4,
        )

    )


def collect_nodes(root):

    python_inventory, python_failed = collect_language_nodes(root, {".py"}, parse_python_file, get_python_children)

    cython_inventory, cython_failed = collect_language_nodes(root, {".pyx", ".pxd", ".pxi"}, parse_cython_file, get_cython_children)

    known_nodes = load_mapping_table()

    python_data = serialize(python_inventory)

    cython_data = serialize(cython_inventory)

    write_json(OUTPUT_DIR / "python_nodes.json", python_data)

    write_json(OUTPUT_DIR / "cython_nodes.json", cython_data)

    write_json(
        OUTPUT_DIR / "python_unknown.json",
        serialize(find_unknown_nodes(python_inventory, known_nodes)),
    )

    write_json(
        OUTPUT_DIR / "cython_unknown.json",
        serialize(find_unknown_nodes(cython_inventory, known_nodes)),
    )

    write_json(OUTPUT_DIR / "python_failed.json", serialize_failed(python_failed))

    write_json(OUTPUT_DIR / "cython_failed.json", serialize_failed(cython_failed))