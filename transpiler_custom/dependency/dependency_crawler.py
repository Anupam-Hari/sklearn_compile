from __future__ import annotations

import ast
from pathlib import Path

from transpiler_custom.parser.python_parser import parse_python_file
from transpiler_custom.parser.cython_pxd_parser import parse_cython_pxd
from transpiler_custom.parser.cython_pyx_parser import parse_cython_pyx


ROOT = Path(
    "/home/anupam/Anupam/sklearn_compile/sklearn"
).resolve()

START = ROOT / "ensemble" / "_forest.py"


py_files = set()
pyx_files = set()
pxd_files = set()
external_modules = set()

visited = set()


def module_to_paths(module_name: str):

    relative = Path(*module_name.split("."))

    return [
        ROOT.parent / f"{relative}.py",
        ROOT.parent / f"{relative}.pyx",
        ROOT.parent / f"{relative}.pxd",
        ROOT.parent / relative / "__init__.py",
    ]


def resolve_relative_module(path, module, level):

    parts = list(path.relative_to(ROOT.parent).with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    if level:

        parts = parts[: -level]

    if module:

        parts.extend(module.split("."))

    return ".".join(parts)


def parse_python_imports(path):

    tree = parse_python_file(path)

    imports = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:

                imports.add(alias.name)

        elif isinstance(node, ast.ImportFrom):

            module = resolve_relative_module(
                path,
                node.module,
                node.level,
            )

            imports.add(module)

    return imports


def walk_cython(node, imports):

    node_type = type(node).__name__

    if node_type == "CImportStatNode":

        imports.add(node.module_name)

    elif node_type == "FromCImportStatNode":

        imports.add(node.module_name)

    elif node_type == "FromImportStatNode":

        imports.add(node.module_name)

    for child_attr in getattr(node, "child_attrs", ()):

        value = getattr(node, child_attr, None)

        if isinstance(value, list):

            for item in value:

                if hasattr(item, "child_attrs"):

                    walk_cython(item, imports)

        elif hasattr(value, "child_attrs"):

            walk_cython(value, imports)


def parse_cython_imports(path):

    if path.suffix == ".pyx":

        tree = parse_cython_pyx(path)

    else:

        tree = parse_cython_pxd(path)

    imports = set()

    walk_cython(tree, imports)

    return imports


def crawl(path):

    path = path.resolve()

    if path in visited:

        return

    visited.add(path)

    if path.suffix == ".py":

        py_files.add(path)

        imports = parse_python_imports(path)

    elif path.suffix == ".pyx":

        pyx_files.add(path)

        imports = parse_cython_imports(path)

    elif path.suffix == ".pxd":

        pxd_files.add(path)

        imports = parse_cython_imports(path)

    else:

        return

    for module in imports:

        if not module:

            continue

        if not module.startswith("sklearn"):

            external_modules.add(module)

            continue

        found = False

        for candidate in module_to_paths(module):

            if candidate.exists():

                found = True

                crawl(candidate)

        if not found:

            external_modules.add(module)


crawl(START)

print("\n=== .py ===\n")

for path in sorted(py_files):

    print(path.relative_to(ROOT.parent))

print("\n=== .pyx ===\n")

for path in sorted(pyx_files):

    print(path.relative_to(ROOT.parent))

print("\n=== .pxd ===\n")

for path in sorted(pxd_files):

    print(path.relative_to(ROOT.parent))

print("\n=== external ===\n")

for module in sorted(external_modules):

    print(module)