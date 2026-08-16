from pathlib import Path

from Cython.Compiler.TreeFragment import StringParseContext, parse_from_strings

from transpiler.ast.nodes import ClassNode, FunctionNode, ModuleNode


def _get_named_member(node):
    for attr in ("name", "class_name", "func_name", "cname"):
        value = getattr(node, attr, None)
        if value:
            return value

    declarator = getattr(node, "declarator", None)
    if declarator is not None:
        if hasattr(declarator, "declared_name"):
            value = declarator.declared_name()
            if value:
                return value
        value = getattr(declarator, "name", None)
        if value:
            return value

    return "unknown"


def _convert_cython_tree_to_ast(tree) -> ModuleNode:
    """Convert the built-in Cython compiler tree to the project’s generic AST."""
    module = ModuleNode()
    body = getattr(tree, "body", None)
    stats = getattr(body, "stats", None) if body is not None else None
    if stats is None:
        stats = []

    for stat in stats:
        stat_type = type(stat).__name__
        if stat_type == "CClassDefNode" or hasattr(stat, "class_name"):
            class_name = getattr(stat, "class_name", None) or getattr(stat, "name", None) or "unknown"
            cls = ClassNode(name=class_name, bases=[], methods=[])
            member_body = getattr(stat, "body", None)
            member_stats = getattr(member_body, "stats", None) if member_body is not None else None
            for member in member_stats or []:
                member_type = type(member).__name__
                if member_type in {"CFuncDefNode", "DefNode"}:
                    method_name = _get_named_member(member)
                    func = FunctionNode(name=method_name)
                    cls.methods.append(func)
                    cls.children.append(func)
            module.children.append(cls)
            module.classes.append(cls)
            continue

        if stat_type in {"DefNode", "CFuncDefNode"}:
            func_name = _get_named_member(stat)
            func = FunctionNode(name=func_name)
            module.children.append(func)
            module.functions.append(func)

    return module


def parse_cython_file(path: str | Path) -> ModuleNode:
    """Parse a .pyx file using Cython’s built-in compiler and normalize it to the project AST."""
    path = Path(path).resolve()
    source = path.read_text(encoding="utf-8")
    context = StringParseContext(str(path))
    tree = parse_from_strings(name=str(path), code=source, context=context)
    return _convert_cython_tree_to_ast(tree)