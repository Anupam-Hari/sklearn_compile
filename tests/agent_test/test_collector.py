from pathlib import Path

from transpiler.ast.inventory.collector import (
    collect_nodes,
)


collect_nodes(
    Path("sklearn"),
)