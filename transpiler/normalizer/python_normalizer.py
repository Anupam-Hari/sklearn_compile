import ast

from transpiler.ast.nodes import (
    ASTNode,
    AssignmentNode,
    CallNode,
    ClassNode,
    ForNode,
    FunctionNode,
    IfNode,
    ImportNode,
    ModuleNode,
    ReturnNode,
    VariableNode,
    WhileNode,
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

def normalize_statement(node):

    if isinstance(node, ast.Assign):

        if node.targets and isinstance(node.targets[0], ast.Name):
            return AssignmentNode(
                name=node.targets[0].id,
                attributes={
                    "target": node.targets[0].id,
                    "value": ast.unparse(node.value),
                },
            )

    elif isinstance(node, ast.Return):

        value = None

        if node.value:
            value = ast.unparse(node.value)

        return ReturnNode(value=value)

    elif isinstance(node, ast.Call):

        if isinstance(node.func, ast.Name):

            return CallNode(
                name=node.func.id,
                attributes={
                    "name": node.func.id,
                    "args": [
                        ast.unparse(arg)
                        for arg in node.args
                    ],
                },
            )

    elif isinstance(node, ast.If):

        children = []

        for child in node.body:
            normalized = normalize_statement(child)

            if normalized:
                children.append(normalized)

        return IfNode(
            condition=ast.unparse(node.test),
            children=children,
        )

    elif isinstance(node, ast.For):

        children = []

        for child in node.body:
            normalized = normalize_statement(child)

            if normalized:
                children.append(normalized)

        target = None

        if isinstance(node.target, ast.Name):
            target = node.target.id

        iterator = ast.unparse(node.iter)

        print(
            target,
            iterator,
        )

        return ForNode(
            target=target,
            attributes={
                "iterator": iterator,
            },
            children=children,
        )

    elif isinstance(node, ast.While):

        children = []

        for child in node.body:
            normalized = normalize_statement(child)

            if normalized:
                children.append(normalized)

        condition = ast.unparse(node.test)

        return WhileNode(
            condition=condition,
            children=children,
        )

    elif isinstance(node, ast.Break):

        return ASTNode(
            node_type="break",
            name="break",
        )

    elif isinstance(node, ast.Continue):

        return ASTNode(
            node_type="continue",
            name="continue",
        )

    elif isinstance(node, ast.Expr):

        return normalize_statement(node.value)

    return None

def normalize_function(node: ast.FunctionDef) -> FunctionNode:

    children = []

    for statement in node.body:

        normalized = normalize_statement(statement)

        if normalized:
            children.append(normalized)

    return FunctionNode(
        name=node.name,
        children=children,
    )


def normalize_class(node: ast.ClassDef):
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
        children=methods,
    )


def normalize_module(tree: ast.Module) -> ModuleNode:
    module = ModuleNode()

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module.children.append(normalize_import(node))

        elif isinstance(node, ast.ClassDef):
            module.children.append(normalize_class(node))

        elif isinstance(node, ast.FunctionDef):
            module.children.append(normalize_function(node))

    return module


def normalize_python_ast(tree: ast.Module) -> ModuleNode:
    return normalize_module(tree)