from transpiler.ir.models import IROperation


def begin_loop(name: str) -> IROperation:
    return IROperation(
        opcode="BeginLoop",
        inputs=[],
        outputs=[],
        attributes={"name": name},
    )


def end_loop(name: str) -> IROperation:
    return IROperation(
        opcode="EndLoop",
        inputs=[],
        outputs=[],
        attributes={"name": name},
    )


def branch(condition: str) -> IROperation:
    return IROperation(
        opcode="Branch",
        inputs=[],
        outputs=[],
        attributes={"condition": condition},
    )


def return_operation(value: str) -> IROperation:
    return IROperation(
        opcode="Return",
        inputs=[value],
        outputs=[],
    )