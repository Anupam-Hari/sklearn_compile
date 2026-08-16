from pathlib import Path

from transpiler.ast.nodes import ModuleNode
from transpiler.dependency.models import Symbol


def extract_symbols(
    module: ModuleNode,
    file_path: Path,
    language: str = "python",
) -> list[Symbol]:

    symbols = []

    for cls in module.classes:
        symbols.append(
            Symbol(
                name=cls.name,
                symbol_type="class",
                file_path=file_path,
                language=language,
                base_class=(
                    cls.bases[0]
                    if cls.bases
                    else None
                ),
            )
        )

        for method in cls.methods:
            symbols.append(
                Symbol(
                    name=method.name,
                    symbol_type="method",
                    file_path=file_path,
                    language=language,
                    parent=cls.name,
                )
            )

    for function in module.functions:
        symbols.append(
            Symbol(
                name=function.name,
                symbol_type="function",
                file_path=file_path,
                language=language,
            )
        )

    return symbols