from transpiler.ir.builder import (
    create_node,
    evaluate_split,
    partition_samples,
)
from transpiler.ir.control import (
    begin_loop,
    branch,
    end_loop,
)
from transpiler.ir.graph import IRGraph


class CythonMethodVisitor:

    def __init__(self):
        self.graph = IRGraph()

    def visit(self, source: str):

        lines = source.splitlines()

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("while "):
                self.graph.add(begin_loop("while"))

            elif stripped.startswith("if "):
                self.graph.add(branch(stripped))

            elif "splitter.node_split(" in stripped:
                self.graph.add(evaluate_split())

            elif "tree._add_node(" in stripped:
                self.graph.add(create_node())

            elif "partition_samples" in stripped:
                self.graph.add(partition_samples())

        return self.graph