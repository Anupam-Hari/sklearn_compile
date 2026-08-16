from transpiler.cython.nodes import (
    BlockNode,
    CallNode,
    ReturnNode,
)

from transpiler.ir.graph import IRGraph
from transpiler.ir.control import (
    begin_loop,
    end_loop,
    branch,
    return_operation,
)

from transpiler.ir.models import IROperation
from transpiler.cython.operation_map import OPERATION_MAP


def build_ir(node, graph=None):

    if graph is None:
        graph = IRGraph()

    if isinstance(node, BlockNode):

        if node.kind == "while":

            graph.add(
                begin_loop("while")
            )

        elif node.kind == "for":

            graph.add(
                begin_loop("for")
            )

        elif node.kind == "if":

            graph.add(
                branch(node.condition)
            )

        for child in node.children:

            build_ir(
                child,
                graph,
            )

        if node.kind == "while":

            graph.add(
                end_loop("while")
            )

        elif node.kind == "for":

            graph.add(
                end_loop("for")
            )

    elif isinstance(node, CallNode):

        if node.name in OPERATION_MAP:

            graph.add(
                IROperation(
                    opcode=OPERATION_MAP[node.name],
                    inputs=[],
                    outputs=[],
                )
            )

    elif isinstance(node, ReturnNode):

        graph.add(
            return_operation(
                node.value
            )
        )

    return graph