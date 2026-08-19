import ast

from transpiler_custom.mapping.references import (
    CYTHON_REFERENCES,
    PYTHON_REFERENCES,
)
from transpiler_custom.models.references import (
    ReferenceNode,
)


def normalize_references(
    tree,
    source_file,
):

    normalized = []

    def walk(node):

        node_type = type(node).__name__

        if node_type in PYTHON_REFERENCES:

            reference = normalize_python_reference(
                node,
                source_file,
            )

            if reference:

                normalized.append(reference)

        elif node_type in CYTHON_REFERENCES:

            reference = normalize_cython_reference(
                node,
                source_file,
            )

            if reference:

                normalized.append(reference)

        if isinstance(node, ast.AST):

            for child in ast.iter_child_nodes(node):

                walk(child)

            return

        for child_attr in getattr(
            node,
            "child_attrs",
            (),
        ):

            value = getattr(
                node,
                child_attr,
                None,
            )

            if isinstance(value, list):

                for item in value:

                    if hasattr(
                        item,
                        "child_attrs",
                    ):

                        walk(item)

            elif hasattr(
                value,
                "child_attrs",
            ):

                walk(value)

    walk(tree)

    return normalized


def normalize_python_reference(
    node,
    source_file,
):

    if isinstance(node, ast.Name):

        return ReferenceNode(
            name=node.id,
            kind="NameReference",
            source_file=source_file,
        )

    if isinstance(node, ast.Attribute):

        return ReferenceNode(
            name=node.attr,
            kind="AttributeReference",
            source_file=source_file,
        )

    if isinstance(node, ast.Call):

        function = node.func

        if isinstance(
            function,
            ast.Name,
        ):

            name = function.id

        elif isinstance(
            function,
            ast.Attribute,
        ):

            name = function.attr

        else:

            return None

        return ReferenceNode(
            name=name,
            kind="CallReference",
            source_file=source_file,
        )

    return None


def normalize_cython_reference(
    node,
    source_file,
):

    node_type = type(node).__name__

    if node_type == "NameNode":

        return ReferenceNode(
            name=node.name,
            kind="NameReference",
            source_file=source_file,
        )

    if node_type == "AttributeNode":

        return ReferenceNode(
            name=node.attribute,
            kind="AttributeReference",
            source_file=source_file,
        )

    if node_type in {

        "SimpleCallNode",

        "GeneralCallNode",

    }:

        function = node.function

        if hasattr(
            function,
            "name",
        ):

            name = function.name

        elif hasattr(
            function,
            "attribute",
        ):

            name = function.attribute

        else:

            return None

        return ReferenceNode(
            name=name,
            kind="CallReference",
            source_file=source_file,
        )

    return None