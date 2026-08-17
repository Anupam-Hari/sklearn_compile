from transpiler.dependency.models import Call


def extract_calls(module):

    calls = []

    walk(
        module,
        calls,
    )

    return calls


def walk(
    node,
    calls,
    parent_class=None,
    parent_function=None,
):

    current_class = parent_class
    current_function = parent_function

    if node.node_type == "class":

        current_class = node.name

    elif node.node_type == "function":

        current_function = node.name

    elif node.node_type == "call":

        calls.append(
            Call(
                name=node.name,
                parent_class=current_class,
                parent_function=current_function,
            )
        )

    for child in node.children:

        walk(
            child,
            calls,
            current_class,
            current_function,
        )