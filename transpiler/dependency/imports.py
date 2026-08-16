from transpiler.ast.nodes import ModuleNode
from transpiler.dependency.models import ImportSymbol


def extract_imports(
    module: ModuleNode,
) -> list[ImportSymbol]:

    imports = []

    for node in module.children:

        if node.node_type != "import":
            continue

        if node.module:

            for name in node.names:

                imports.append(
                    ImportSymbol(
                        module=node.module,
                        name=name,
                    )
                )

        else:

            for name in node.names:

                imports.append(
                    ImportSymbol(
                        module=name,
                    )
                )

    return imports