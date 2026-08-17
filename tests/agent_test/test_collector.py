from pathlib import Path

from transpiler.agent.tools.collector import (
    collect_nodes,
)


collect_nodes(
    Path("sklearn"),
)