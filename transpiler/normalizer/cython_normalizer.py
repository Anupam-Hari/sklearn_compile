from transpiler.ast.mapping_table import CYTHON_TO_NORMALIZED
from transpiler.ast.unsupported_nodes import UNSUPPORTED_CYTHON_NODES
from transpiler.ast.nodes import (
    ClassNode,
    FunctionNode,
    ImportNode,
    ModuleNode,
)


def _get_name(node):

    for attr in (
        "name",
        "class_name",
        "func_name",
        "cname",
    ):

        value = getattr(node, attr, None)

        if value:
            return value

    declarator = getattr(node, "declarator", None)

    if declarator is not None:

        if hasattr(
            declarator,
            "declared_name",
        ):

            try:

                value = declarator.declared_name()

                if value:
                    return value

            except Exception:
                pass

        value = getattr(
            declarator,
            "name",
            None,
        )

        if value:
            return value

    return "unknown"


def normalize_import(node):

    node_type = type(node).__name__

    if node_type == "ImportNode":

        names = []

        for item in getattr(node, "items", []):

            if isinstance(item, tuple):

                names.append(item[1])

            else:

                name = _get_name(item)

                if name != "unknown":

                    names.append(name)

        return ImportNode(
            module="",
            names=names,
        )

    module_name = getattr(
        node,
        "module_name",
        "",
    )

    names = []

    for item in getattr(
        node,
        "imported_names",
        [],
    ):

        if isinstance(item, tuple):

            names.append(item[1])

        else:

            names.append(_get_name(item))

    return ImportNode(
        module=module_name,
        names=names,
    )


def normalize_function(node):

    return FunctionNode(
        name=_get_name(node),
    )


def normalize_class(node):

    cls = ClassNode(
        name=_get_name(node),
        bases=[],
        methods=[],
    )

    body = getattr(
        node,
        "body",
        None,
    )

    stats = getattr(
        body,
        "stats",
        [],
    )

    for child in stats:

        child_type = type(child).__name__

        if child_type in {
            "DefNode",
            "CFuncDefNode",
        }:

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


def normalize_cython_ast(tree):

    module = ModuleNode()

    body = getattr(
        tree,
        "body",
        None,
    )

    stats = getattr(
        body,
        "stats",
        [],
    )

    for node in stats:

        node_type = type(node).__name__

        if node_type in UNSUPPORTED_CYTHON_NODES:
            continue

        normalized_type = CYTHON_TO_NORMALIZED.get(
            node_type
        )

        if normalized_type == "ImportNode":

            module.add_child(
                normalize_import(node)
            )

        elif normalized_type == "ClassNode":

            module.add_child(
                normalize_class(node)
            )

        elif normalized_type == "FunctionNode":

            module.add_child(
                normalize_function(node)
            )

    return module