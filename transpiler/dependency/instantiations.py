import ast
from collections import defaultdict
from pathlib import Path


def extract_instantiations(path: Path):

    source = path.read_text()

    tree = ast.parse(source)

    instances = defaultdict(set)

    class Visitor(ast.NodeVisitor):

        def visit_Assign(self, node):

            if not isinstance(node.value, ast.Call):
                return

            if not isinstance(node.value.func, ast.Name):
                return

            constructor = node.value.func.id

            for target in node.targets:

                if isinstance(target, ast.Name):

                    instances[target.id].add(
                        constructor
                    )

            self.generic_visit(node)

    Visitor().visit(tree)

    return dict(instances)