import ast

from transpiler_custom.models.imports import ImportNode
from transpiler_custom.mapping.imports import (
    CYTHON_IMPORTS,
    PYTHON_IMPORTS,
)


def normalize_imports(tree, source_file):

    normalized = []

    def walk(node):

        node_type = type(node).__name__

        if node_type in PYTHON_IMPORTS:

            normalized.extend(
                normalize_python_import(node, source_file)
            )

        elif node_type in CYTHON_IMPORTS:

            normalized.extend(
                normalize_cython_import(node, source_file)
            )

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


def normalize_python_import(node, source_file):

    imports = []

    if isinstance(node, ast.Import):

        for alias in node.names:

            imports.append(
                ImportNode(
                    module=alias.name,
                    symbols=[],
                    alias=alias.asname,
                    level=0,
                    is_cimport=False,
                    source_file=str(source_file),
                )
            )

    elif isinstance(node, ast.ImportFrom):

        imports.append(
            ImportNode(
                module=node.module or "",
                symbols=[
                    alias.name
                    for alias in node.names
                ],
                alias=None,
                level=node.level,
                is_cimport=False,
                source_file=str(source_file),
            )
        )

    return imports


def normalize_cython_import(node, source_file):

    imports = []

    node_type = type(node).__name__

    if node_type == "ImportNode":

        module_name = getattr(
            node.module_name,
            "value",
            str(node.module_name),
        )

        imports.append(
            ImportNode(
                module=module_name,
                symbols=[],
                alias=None,
                level=node.level,
                is_cimport=False,
                source_file=str(source_file),
            )
        )

    elif node_type == "CImportStatNode":

        imports.append(
            ImportNode(
                module=node.module_name,
                symbols=[],
                alias=node.as_name,
                level=0,
                is_cimport=True,
                source_file=str(source_file),
            )
        )

    elif node_type == "FromCImportStatNode":

        imports.append(
            ImportNode(
                module=node.module_name,
                symbols=[
                    imported[1]
                    for imported in node.imported_names
                ],
                alias=None,
                level=node.relative_level,
                is_cimport=True,
                source_file=str(source_file),
            )
        )

    return imports