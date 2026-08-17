import ast

from transpiler.ast.mapping_table import PYTHON_TO_NORMALIZED
from transpiler.ast.nodes import (
    ClassNode,
    FunctionNode,
    ImportNode,
    ModuleNode,
)


def normalize_import(node):

    if isinstance(node, ast.Import):

        return ImportNode(
            module="",
            names=[
                alias.name
                for alias in node.names
            ],
        )

    return ImportNode(
        module=node.module or "",
        names=[
            alias.name
            for alias in node.names
        ],
    )


def normalize_function(node):

    return FunctionNode(
        name=node.name,
    )


def normalize_class(node):

    bases = []

    for base in node.bases:

        try:

            bases.append(
                ast.unparse(base)
            )

        except Exception:

            pass

    cls = ClassNode(
        name=node.name,
        bases=bases,
        methods=[],
    )

    for child in node.body:

        child_type = type(child).__name__

        normalized_type = PYTHON_TO_NORMALIZED.get(
            child_type,
        )

        if normalized_type == "FunctionNode":

            method = normalize_function(
                child,
            )

            cls.methods.append(
                method,
            )

            cls.children.append(
                method,
            )

    return cls


def normalize_python_ast(tree):

    module = ModuleNode()

    for node in tree.body:

        if isinstance(node, (ast.Import, ast.ImportFrom)):

            module.add_child(
                normalize_import(node)
            )

        elif isinstance(node, ast.ClassDef):

            module.add_child(
                normalize_class(node)
            )

        elif isinstance(node, ast.FunctionDef):

            module.add_child(
                normalize_function(node)
            )

    return module