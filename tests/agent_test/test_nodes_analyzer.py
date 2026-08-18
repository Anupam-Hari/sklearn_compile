from pprint import pprint

from transpiler.agent.tools.nodes_analyzer import (
    get_missing_nodes,
)

from transpiler.ast.mapping_table import (
    NODE_MAPPING,
)


pprint(
    get_missing_nodes(
        NODE_MAPPING,
    )
)