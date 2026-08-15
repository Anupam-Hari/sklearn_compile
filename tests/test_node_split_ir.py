from transpiler.ir.builder import (
    extract_feature_column,
    sort_samples,
    evaluate_split,
    partition_samples,
    create_node,
)

from transpiler.ir.control import (
    begin_loop,
    end_loop,
    branch,
    return_operation,
)

from transpiler.ir.graph import IRGraph


graph = IRGraph()

graph.add(begin_loop("candidate_features"))

graph.add(extract_feature_column(0))
graph.add(sort_samples())

graph.add(begin_loop("candidate_thresholds"))

graph.add(evaluate_split())

graph.add(branch("improvement > best"))

graph.add(end_loop("candidate_thresholds"))

graph.add(partition_samples())

graph.add(create_node())

graph.add(end_loop("candidate_features"))

graph.add(return_operation("best_split"))

graph.dump()