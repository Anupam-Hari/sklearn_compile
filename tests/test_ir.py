from transpiler.ir.builder import (
    create_node,
    evaluate_split,
    extract_feature_column,
    partition_samples,
    sort_samples,
)

from transpiler.ir.models import IRModule


module = IRModule()

module.add(extract_feature_column(0))
module.add(sort_samples())
module.add(evaluate_split())
module.add(partition_samples())
module.add(create_node())

for operation in module.operations:
    print(operation)