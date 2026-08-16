from transpiler.ir.builder import (
    create_node,
    evaluate_split,
    partition_samples,
    sort_samples,
)

from transpiler.ir.models import (
    IROperation,
)

from transpiler.ir.control import (
    begin_loop,
    branch,
    end_loop,
    return_operation,
)


OPERATION_MAP = {
    "splitter.node_split": evaluate_split,
    "tree._add_node": create_node,
    "tree._resize": lambda: IROperation(
        opcode="ResizeTree",
        inputs=[],
        outputs=[],
    ),
    "tree._resize_c": lambda: IROperation(
        opcode="ResizeTree",
        inputs=[],
        outputs=[],
    ),
    "builder_stack.push": lambda: IROperation(
        opcode="PushStack",
        inputs=[],
        outputs=[],
    ),
    "builder_stack.pop": lambda: IROperation(
        opcode="PopStack",
        inputs=[],
        outputs=[],
    ),
    "builder_stack.top": lambda: IROperation(
        opcode="PeekStack",
        inputs=[],
        outputs=[],
    ),
}