import ast
from pathlib import Path


def extract_function_calls(path: Path) -> dict[str, list[str]]:

    source = path.read_text()

    tree = ast.parse(source)

    calls = {}

    class Visitor(ast.NodeVisitor):

        def __init__(self):

            self.current_function = None

        def visit_FunctionDef(self, node):

            self.current_function = node.name

            calls[self.current_function] = []

            self.generic_visit(node)

        def visit_Call(self, node):

            if self.current_function is None:
                return

            if isinstance(node.func, ast.Name):

                calls[self.current_function].append(
                    node.func.id
                )

            elif isinstance(node.func, ast.Attribute):

                calls[self.current_function].append(
                    node.func.attr
                )

            self.generic_visit(node)

    Visitor().visit(tree)

    return calls