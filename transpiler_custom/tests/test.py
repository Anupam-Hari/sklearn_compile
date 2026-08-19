from __future__ import annotations

import ast
from collections import deque
from dataclasses import dataclass
from pathlib import Path


SKLEARN_ROOT = Path("/home/anupam/Anupam/sklearn_compile/sklearn")
Path.resolve(SKLEARN_ROOT)


# ---------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------

@dataclass
class ImportInfo:
    module: str
    file: Path | None


@dataclass
class FunctionInfo:
    name: str
    node: ast.FunctionDef
    owner: str | None = None


@dataclass
class ClassInfo:
    name: str
    node: ast.ClassDef
    bases: list[str]
    methods: dict[str, FunctionInfo]


@dataclass
class ModuleInfo:
    path: Path
    imports: dict[str, ImportInfo]
    functions: dict[str, FunctionInfo]
    classes: dict[str, ClassInfo]


module_cache: dict[Path, ModuleInfo] = {}


# ---------------------------------------------------------------------
# Import resolution
# ---------------------------------------------------------------------

def module_name_from_path(path: Path) -> str:
    rel = path.relative_to(SKLEARN_ROOT.parent)
    return ".".join(rel.with_suffix("").parts)


def resolve_module_to_file(module: str) -> Path | None:
    parts = module.split(".")

    py = SKLEARN_ROOT.parent.joinpath(*parts).with_suffix(".py")
    if py.exists():
        return py

    pyx = SKLEARN_ROOT.parent.joinpath(*parts).with_suffix(".pyx")
    if pyx.exists():
        return pyx

    init = SKLEARN_ROOT.parent.joinpath(*parts, "__init__.py")
    if init.exists():
        return init

    return None


def resolve_relative_import(
    current_file: Path,
    module: str | None,
    level: int,
) -> str:

    current_module = module_name_from_path(current_file)
    parts = current_module.split(".")[:-1]

    if level:
        parts = parts[:-level + 1]

    if module:
        parts += module.split(".")

    return ".".join(parts)


# ---------------------------------------------------------------------
# AST parsing
# ---------------------------------------------------------------------

def parse_module(path: Path) -> ModuleInfo:

    if path in module_cache:
        return module_cache[path]

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    imports = {}
    functions = {}
    classes = {}

    for node in tree.body:

        if isinstance(node, ast.Import):

            for alias in node.names:

                imports[alias.asname or alias.name.split(".")[-1]] = (
                    ImportInfo(
                        alias.name,
                        resolve_module_to_file(alias.name),
                    )
                )

        elif isinstance(node, ast.ImportFrom):

            abs_module = resolve_relative_import(
                path,
                node.module,
                node.level,
            )

            target_file = resolve_module_to_file(abs_module)

            for alias in node.names:

                imports[alias.asname or alias.name] = ImportInfo(
                    abs_module,
                    target_file,
                )

        elif isinstance(node, ast.FunctionDef):

            functions[node.name] = FunctionInfo(
                node.name,
                node,
            )

        elif isinstance(node, ast.ClassDef):

            bases = []

            for base in node.bases:

                if isinstance(base, ast.Name):
                    bases.append(base.id)

                elif isinstance(base, ast.Attribute):
                    bases.append(base.attr)

            methods = {}

            for item in node.body:

                if isinstance(item, ast.FunctionDef):

                    methods[item.name] = FunctionInfo(
                        item.name,
                        item,
                        node.name,
                    )

            classes[node.name] = ClassInfo(
                node.name,
                node,
                bases,
                methods,
            )

    info = ModuleInfo(
        path,
        imports,
        functions,
        classes,
    )

    module_cache[path] = info

    return info


# ---------------------------------------------------------------------
# Inheritance resolution
# ---------------------------------------------------------------------

def find_method(
    cls_name: str,
    method_name: str,
    module: ModuleInfo,
):

    cls = module.classes.get(cls_name)

    if not cls:
        return None

    if method_name in cls.methods:
        return cls.methods[method_name], module.path

    for base_name in cls.bases:

        imported = module.imports.get(base_name)

        if not imported or not imported.file:
            continue

        base_module = parse_module(imported.file)

        result = find_method(
            base_name,
            method_name,
            base_module,
        )

        if result:
            return result

    return None


# ---------------------------------------------------------------------
# Dependency extraction
# ---------------------------------------------------------------------

class CallCollector(ast.NodeVisitor):

    def __init__(self):
        self.calls = set()

    def visit_Call(self, node):

        if isinstance(node.func, ast.Name):

            self.calls.add(node.func.id)

        elif isinstance(node.func, ast.Attribute):

            self.calls.add(node.func.attr)

        self.generic_visit(node)


# ---------------------------------------------------------------------
# Recursive traversal
# ---------------------------------------------------------------------

def collect_dependencies():

    start_file = SKLEARN_ROOT / "ensemble" / "_forest.py"

    root = parse_module(start_file)

    queue = deque()

    queue.append(
        find_method(
            "RandomForestClassifier",
            "fit",
            root,
        )
    )

    queue.append(
        find_method(
            "RandomForestClassifier",
            "predict",
            root,
        )
    )

    visited_files = set()
    visited_symbols = set()

    while queue:

        item = queue.popleft()

        if not item:
            continue

        func, path = item

        key = (path, func.name)

        if key in visited_symbols:
            continue

        visited_symbols.add(key)
        visited_files.add(path)

        collector = CallCollector()
        collector.visit(func.node)

        module = parse_module(path)

        for call in collector.calls:

            if call in module.functions:

                queue.append(
                    (
                        module.functions[call],
                        path,
                    )
                )

            for cls in module.classes.values():

                if call in cls.methods:

                    queue.append(
                        (
                            cls.methods[call],
                            path,
                        )
                    )

            imported = module.imports.get(call)

            if imported and imported.file:

                imported_module = parse_module(
                    imported.file
                )

                visited_files.add(
                    imported_module.path
                )

    return sorted(visited_files)


if __name__ == "__main__":

    files = collect_dependencies()

    for f in files:
        print(f)