import re

from transpiler.ast.nodes import (
    ClassNode,
    FunctionNode,
    ImportNode,
    ModuleNode,
)


IMPORT_RE = re.compile(
    r"from\s+([\w\.]+)\s+(?:cimport|import)\s+\((.*?)\)",
    re.DOTALL,
)

CLASS_RE = re.compile(
    r"cdef\s+class\s+(\w+)(?:\((.*?)\))?"
)

FUNCTION_RE = re.compile(
    r"(?:cdef|cpdef|def)\s+(\w+)\s*\("
)


def normalize_cython_source(
    source: str,
) -> ModuleNode:

    module = ModuleNode()

    for match in IMPORT_RE.finditer(source):

        imported_module = match.group(1)

        names = [
            name.strip()
            for name in match.group(2).split(",")
            if name.strip()
        ]

        module.imports.append(
            ImportNode(
                module=imported_module,
                names=names,
            )
        )

    classes = []

    for match in CLASS_RE.finditer(source):

        bases = []

        if match.group(2):

            bases = [
                base.strip()
                for base in match.group(2).split(",")
                if base.strip()
            ]

        cls = ClassNode(
            name=match.group(1),
            bases=bases,
            methods=[],
        )

        classes.append(cls)

        module.classes.append(cls)

    current_class = None

    lines = source.splitlines()

    for line in lines:

        class_match = CLASS_RE.match(
            line.strip()
        )

        if class_match:

            class_name = class_match.group(1)

            current_class = next(
                (
                    cls
                    for cls in classes
                    if cls.name == class_name
                ),
                None,
            )

            continue

        function_match = FUNCTION_RE.match(
            line.strip()
        )

        if not function_match:
            continue

        function = FunctionNode(
            name=function_match.group(1),
        )

        if current_class:

            current_class.methods.append(
                function
            )

        else:

            module.functions.append(
                function
            )

    return module