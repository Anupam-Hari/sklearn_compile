import ast
from pathlib import Path

from transpiler.ir.builder import (
    create_node,
    evaluate_split,
    extract_feature_column,
    partition_samples,
    sort_samples,
)
from transpiler.ir.control import (
    begin_loop,
    branch,
    end_loop,
    return_operation,
)
from transpiler.ir.graph import IRGraph


class SplitterParser(ast.NodeVisitor):

    def __init__(self):
        self.graph = IRGraph()

    def visit_For(self, node):
        self.graph.add(begin_loop("for"))
        self.generic_visit(node)
        self.graph.add(end_loop("for"))

    def visit_While(self, node):
        self.graph.add(begin_loop("while"))
        self.generic_visit(node)
        self.graph.add(end_loop("while"))

    def visit_If(self, node):
        condition = ast.unparse(node.test)
        self.graph.add(branch(condition))
        self.generic_visit(node)

    def visit_Return(self, node):
        value = ast.unparse(node.value) if node.value else ""
        self.graph.add(return_operation(value))

    def visit_Call(self, node):

        if isinstance(node.func, ast.Name):

            name = node.func.id

            if name == "sort_samples_and_feature_values":
                self.graph.add(sort_samples())

            elif name == "partition_samples_final":
                self.graph.add(partition_samples())

            elif name == "proxy_impurity_improvement":
                self.graph.add(evaluate_split())

        self.generic_visit(node)


def parse_file(path: str):

    source = Path(path).read_text()

    tree = ast.parse(source)

    parser = SplitterParser()

    parser.visit(tree)

    return parser.graph