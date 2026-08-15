import ast

from transpiler.ast.nodes import (
    ClassNode,
    FunctionNode,
    ImportNode,
    ModuleNode,
)


def normalize_import(node: ast.Import | ast.ImportFrom) -> ImportNode:
    if isinstance(node, ast.Import):
        return ImportNode(
            module="",
            names=[alias.name for alias in node.names],
        )

    return ImportNode(
        module=node.module or "",
        names=[alias.name for alias in node.names],
    )


def normalize_function(node: ast.FunctionDef) -> FunctionNode:
    return FunctionNode(
        name=node.name,
    )


def normalize_class(node: ast.ClassDef) -> ClassNode:
    bases = []

    for base in node.bases:
        if isinstance(base, ast.Name):
            bases.append(base.id)

    methods = []

    for child in node.body:
        if isinstance(child, ast.FunctionDef):
            methods.append(normalize_function(child))

    return ClassNode(
        name=node.name,
        bases=bases,
        methods=methods,
    )


def normalize_module(tree: ast.Module) -> ModuleNode:
    module = ModuleNode()

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module.imports.append(normalize_import(node))

        elif isinstance(node, ast.ClassDef):
            module.classes.append(normalize_class(node))

        elif isinstance(node, ast.FunctionDef):
            module.functions.append(normalize_function(node))

    return module


def normalize_python_ast(tree: ast.Module) -> ModuleNode:
    return normalize_module(tree)