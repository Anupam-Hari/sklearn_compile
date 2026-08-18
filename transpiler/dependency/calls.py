from transpiler.dependency.models import (
    Call,
    DependencyGraph,
)

from transpiler.ast.nodes import (
    CallNode,
    ClassNode,
    FunctionNode,
)


def extract_calls(
    graph: DependencyGraph,
    module,
    file_path,
) -> None:

    graph.calls[file_path] = []

    walk(
        graph,
        module,
        file_path,
    )


def add_call(
    graph,
    file_path,
    call,
):

    graph.calls[
        file_path
    ].append(
        call,
    )


def walk(
    graph,
    node,
    file_path,
    parent_class=None,
    parent_function=None,
):

    current_class = parent_class
    current_function = parent_function

    if isinstance(
        node,
        ClassNode,
    ):

        current_class = node.name

    elif isinstance(
        node,
        FunctionNode,
    ):

        current_function = node.name

    elif isinstance(
        node,
        CallNode,
    ):

        add_call(
            graph,
            file_path,
            Call(
                name=node.name,
                parent_class=current_class,
                parent_function=current_function,
            ),
        )

    for child in node.children:

        walk(
            graph,
            child,
            file_path,
            current_class,
            current_function,
        )