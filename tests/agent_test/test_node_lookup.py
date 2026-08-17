from pprint import pprint

from transpiler.agent.tools.node_lookup import (
    get_node,
)


node = get_node(

    "python",

    "keyword",

)

pprint(node)