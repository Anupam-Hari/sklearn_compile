import ast

from transpiler_custom.mapping.symbols import (
    CYTHON_SYMBOLS,
    PYTHON_SYMBOLS,
)
from transpiler_custom.models.symbols import SymbolNode


PYTHON_PARENTS = {
    "ClassDef",
    "FunctionDef",
}


CYTHON_PARENTS = {
    "DefNode",
    "PyClassDefNode",
    "CFuncDefNode",
    "CClassDefNode",
}


def normalize_symbols(tree, source_file):

    normalized = []

    stack = []

    def current_parent():

        if stack:

            return stack[-1]

        return (None, None)

    def get_cython_name(node):

        node_type = type(node).__name__

        if node_type == "CClassDefNode":

            return node.class_name

        return getattr(node, "name", None)

    def walk(node):

        node_type = type(node).__name__

        entered_parent = False

        if node_type in PYTHON_SYMBOLS:
        
                    symbol = normalize_python_symbol(
                        node,
                        source_file,
                        current_parent(),
                    )
        
                    if symbol:
        
                        normalized.append(symbol)
        
        elif node_type in CYTHON_SYMBOLS:

            symbols = normalize_cython_symbol(
                node,
                source_file,
                current_parent(),
            )

            normalized.extend(symbols)

        if node_type in PYTHON_PARENTS:

            stack.append(
                (
                    node.name,
                    PYTHON_SYMBOLS[node_type],
                )
            )

            entered_parent = True

        elif node_type in CYTHON_PARENTS:

            stack.append(
                (
                    get_cython_name(node),
                    CYTHON_SYMBOLS[node_type],
                )
            )

            entered_parent = True

        if isinstance(node, ast.AST):

            for child in ast.iter_child_nodes(node):

                walk(child)

        else:

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

        if entered_parent:

            stack.pop()

    walk(tree)

    return normalized

def normalize_python_symbol(
    node,
    source_file,
    parent,
):

    parent_name, parent_kind = parent

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
            parent_name=parent_name,
            parent_kind=parent_kind,
        )

    if isinstance(node, ast.FunctionDef):

        return SymbolNode(
            name=node.name,
            kind="FunctionNode",
            source_file=source_file,
            parent_name=parent_name,
            parent_kind=parent_kind,
        )

    return None

def normalize_cython_symbol(
    node,
    source_file,
    parent,
):

    parent_name, parent_kind = parent

    node_type = type(node).__name__

    if node_type == "ModuleNode":

        return [
            SymbolNode(
                name=source_file.stem,
                kind="ModuleNode",
                source_file=source_file,
                parent_name=None,
                parent_kind=None,
            )
        ]

    if node_type == "CClassDefNode":

        return [
            SymbolNode(
                name=node.class_name,
                kind="ClassNode",
                source_file=source_file,
                parent_name=parent_name,
                parent_kind=parent_kind,
            )
        ]

    if node_type == "CTypeDefNode":

        name = getattr(
            node.declarator,
            "name",
            None,
        )

        if name:

            return [
                SymbolNode(
                    name=name,
                    kind="TypeDefinitionNode",
                    source_file=source_file,
                    parent_name=parent_name,
                    parent_kind=parent_kind,
                )
            ]

    if node_type == "CVarDefNode":

        symbols = []

        for declarator in node.declarators:

            name = getattr(
                declarator,
                "name",
                None,
            )

            if name:

                symbols.append(
                    SymbolNode(
                        name=name,
                        kind="VariableNode",
                        source_file=source_file,
                        parent_name=parent_name,
                        parent_kind=parent_kind,
                    )
                )

        return symbols

    name = getattr(
        node,
        "name",
        None,
    )

    if name:

        return [
            SymbolNode(
                name=name,
                kind=CYTHON_SYMBOLS[node_type],
                source_file=source_file,
                parent_name=parent_name,
                parent_kind=parent_kind,
            )
        ]

    return []