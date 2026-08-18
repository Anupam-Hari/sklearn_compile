from transpiler.ast.nodes import ModuleNode
from transpiler.dependency.models import (
    DependencyGraph,
    ImportSymbol,
)


def extract_imports(
    graph: DependencyGraph,
    module: ModuleNode,
    file_path,
) -> None:

    graph.imports[file_path] = []

    walk(
        graph,
        module,
        file_path,
    )


def walk(
    graph,
    node,
    file_path,
) -> None:

    if node.node_type == "import":

        if node.module:

            for name in node.names:

                graph.imports[
                    file_path
                ].append(
                    ImportSymbol(
                        module=node.module,
                        name=name,
                    )
                )

        else:

            for name in node.names:

                graph.imports[
                    file_path
                ].append(
                    ImportSymbol(
                        module=name,
                    )
                )

    for child in node.children:

        walk(
            graph,
            child,
            file_path,
        )