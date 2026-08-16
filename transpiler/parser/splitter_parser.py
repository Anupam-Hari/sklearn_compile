import ast
from pathlib import Path

from transpiler.ir.models import IRModule, IROperation


class SplitterParser(ast.NodeVisitor):

    def __init__(self):
        self.graph = IRModule()

    def _add(self, opcode: str, **attrs):
        self.graph.add(IROperation(opcode=opcode, inputs=[], outputs=[], attributes=attrs))

    def visit_For(self, node):
        self._add("BeginLoop", type="for")
        self.generic_visit(node)
        self._add("EndLoop", type="for")

    def visit_While(self, node):
        self._add("BeginLoop", type="while")
        self.generic_visit(node)
        self._add("EndLoop", type="while")

    def visit_If(self, node):
        condition = ast.unparse(node.test)
        self._add("Branch", condition=condition)
        self.generic_visit(node)

    def visit_Return(self, node):
        value = ast.unparse(node.value) if node.value else ""
        self._add("Return", value=value)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name == "sort_samples_and_feature_values":
                self._add("SortSamples")
            elif name == "partition_samples_final":
                self._add("PartitionSamples")
            elif name == "proxy_impurity_improvement":
                self._add("EvaluateSplit")

        self.generic_visit(node)


def parse_file(path: str):
    source = Path(path).read_text()
    tree = ast.parse(source)
    parser = SplitterParser()
    parser.visit(tree)
    return parser.graph