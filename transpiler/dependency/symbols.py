from pathlib import Path

from transpiler.ast.nodes import ModuleNode
from transpiler.dependency.models import Symbol


def extract_symbols(
    module,
    file_path,
    language="python",
):
    symbols = []

    for node in module.children:

        if node.node_type == "class":

            symbols.append(
                Symbol(
                    name=node.name,
                    symbol_type="class",
                    file_path=file_path,
                    language=language,
                    base_class=node.bases[0] if node.bases else None,
                )
            )

            for method in node.methods:

                symbols.append(
                    Symbol(
                        name=method.name,
                        symbol_type="method",
                        file_path=file_path,
                        language=language,
                        parent=node.name,
                    )
                )

        elif node.node_type == "function":

            symbols.append(
                Symbol(
                    name=node.name,
                    symbol_type="function",
                    file_path=file_path,
                    language=language,
                )
            )

    return symbols