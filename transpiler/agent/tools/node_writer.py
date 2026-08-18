# transpiler/agent/tools/node_writer.py

from pathlib import Path
import re


NODES_FILE = (
    Path(__file__).resolve().parent.parent.parent
    / "ast"
    / "nodes.py"
)


def load_nodes():

    return NODES_FILE.read_text()


def save_nodes(content):

    NODES_FILE.write_text(
        content,
    )

def clean_node_code(node_code):

    node_code = node_code.strip()

    node_code = re.sub(
        r"^```(?:python)?\s*",
        "",
        node_code,
    )

    node_code = re.sub(
        r"\s*```$",
        "",
        node_code,
    )

    return node_code.strip()

def append_node(node_code):

    node_code = clean_node_code(
        node_code,
    )

    content = load_nodes()

    if node_code in content:

        return False

    content = content.rstrip()

    content += "\n\n\n"

    content += node_code

    content += "\n"

    save_nodes(
        content,
    )

    return True

def update_nodes(
    llm,
    generate_node,
    get_missing_nodes,
):

    for node_name in get_missing_nodes():

        print(
            f"Generating {node_name}"
        )

        node_code = generate_node(
            llm,
            node_name,
        )

        append_node(
            node_code,
        )