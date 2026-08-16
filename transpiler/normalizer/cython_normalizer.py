from Cython.Compiler.TreeFragment import StringParseContext, parse_from_strings

from transpiler.ast.nodes import ClassNode, FunctionNode, ModuleNode


def normalize_cython_source(source: str) -> ModuleNode:
    """Normalize Cython source by parsing it through Cython’s official tree builder."""
    tree = parse_from_strings(
        name="<memory>",
        code=source,
        context=StringParseContext("<memory>"),
    )

    module = ModuleNode()
    body = getattr(tree, "body", None)
    stats = getattr(body, "stats", None) if body is not None else None
    if stats is None:
        stats = []

    for stat in stats:
        if type(stat).__name__ == "CClassDefNode" or hasattr(stat, "class_name"):
            class_name = getattr(stat, "class_name", None) or getattr(stat, "name", None) or "unknown"
            cls = ClassNode(name=class_name, bases=[], methods=[])
            member_body = getattr(stat, "body", None)
            member_stats = getattr(member_body, "stats", None) if member_body is not None else None
            for member in member_stats or []:
                if type(member).__name__ in {"CFuncDefNode", "DefNode"}:
                    method_name = getattr(member, "name", None)
                    if method_name is None and hasattr(member, "declarator"):
                        method_name = getattr(member.declarator, "name", None)
                    if method_name is None:
                        method_name = "unknown"
                    func = FunctionNode(name=method_name)
                    cls.methods.append(func)
                    cls.children.append(func)
            module.children.append(cls)
            module.classes.append(cls)
        elif type(stat).__name__ in {"DefNode", "CFuncDefNode"}:
            func_name = getattr(stat, "name", None)
            if func_name is None and hasattr(stat, "declarator"):
                func_name = getattr(stat.declarator, "name", None)
            if func_name is None:
                func_name = "unknown"
            func = FunctionNode(name=func_name)
            module.children.append(func)
            module.functions.append(func)

    return module