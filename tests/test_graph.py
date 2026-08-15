from transpiler.ir.builder import (
    extract_feature_column,
    sort_samples,
    evaluate_split,
    partition_samples,
    create_node,
)

from transpiler.ir.graph import IRGraph


graph = IRGraph()

graph.add(extract_feature_column(0))
graph.add(sort_samples())
graph.add(evaluate_split())
graph.add(partition_samples())
graph.add(create_node())

graph.dump()