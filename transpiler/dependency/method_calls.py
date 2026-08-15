import ast
from collections import defaultdict
from pathlib import Path


def extract_method_calls(path: Path):

    source = path.read_text()

    tree = ast.parse(source)

    calls = defaultdict(list)

    class Visitor(ast.NodeVisitor):

        def __init__(self):

            self.current_function = None

        def visit_FunctionDef(self, node):

            self.current_function = node.name

            self.generic_visit(node)

        def visit_Call(self, node):

            if self.current_function is None:
                return

            if isinstance(node.func, ast.Attribute):

                calls[self.current_function].append(
                    (
                        ast.unparse(node.func.value),
                        node.func.attr,
                    )
                )

            self.generic_visit(node)

    Visitor().visit(tree)

    return dict(calls)