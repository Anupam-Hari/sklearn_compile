import ast

from transpiler_custom.mapping.symbols import (
    CYTHON_SYMBOLS,
    PYTHON_SYMBOLS,
)
from transpiler_custom.models.symbols import SymbolNode


def normalize_symbols(tree, source_file):

    normalized = []

    def walk(node):

        node_type = type(node).__name__

        if node_type in PYTHON_SYMBOLS:

            symbol = normalize_python_symbol(
                node,
                source_file,
            )

            if symbol:

                normalized.append(symbol)

        elif node_type in CYTHON_SYMBOLS:

            symbol = normalize_cython_symbol(
                node,
                source_file,
            )

            if symbol:

                normalized.append(symbol)

        if isinstance(node, ast.AST):

            for child in ast.iter_child_nodes(node):

                walk(child)

            return

        for child_attr in getattr(node, "child_attrs", ()):

            value = getattr(node, child_attr, None)

            if isinstance(value, list):

                for item in value:

                    if hasattr(item, "child_attrs"):

                        walk(item)

            elif hasattr(value, "child_attrs"):

                walk(value)

    walk(tree)

    return normalized


def normalize_python_symbol(
    node,
    source_file,
):

    if isinstance(node, ast.Module):

        return SymbolNode(
            name=source_file.stem,
            kind="ModuleNode",
            source_file=source_file,
        )

    if isinstance(node, ast.ClassDef):

        return SymbolNode(
            name=node.name,
            kind="ClassNode",
            source_file=source_file,
        )

    if isinstance(node, ast.FunctionDef):

        return SymbolNode(
            name=node.name,
            kind="FunctionNode",
            source_file=source_file,
        )

    if isinstance(node, ast.Assign):

        if len(node.targets) == 1:

            target = node.targets[0]

            if isinstance(target, ast.Name):

                return SymbolNode(
                    name=target.id,
                    kind="AssignmentNode",
                    source_file=source_file,
                )

    if isinstance(node, ast.AnnAssign):

        if isinstance(node.target, ast.Name):

            return SymbolNode(
                name=node.target.id,
                kind="AssignmentNode",
                source_file=source_file,
            )

    return None


def normalize_cython_symbol(
    node,
    source_file,
):

    node_type = type(node).__name__

    if node_type == "ModuleNode":

        return SymbolNode(
            name=source_file.stem,
            kind="ModuleNode",
            source_file=source_file,
        )

    if hasattr(node, "name"):

        return SymbolNode(
            name=node.name,
            kind=CYTHON_SYMBOLS[node_type],
            source_file=source_file,
        )

    return None