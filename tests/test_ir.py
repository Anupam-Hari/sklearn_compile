from transpiler.ir.models import IRModule, IROperation


module = IRModule()

for opcode in [
    "ExtractFeatureColumn",
    "SortSamples",
    "EvaluateSplit",
    "PartitionSamples",
    "CreateNode",
]:
    module.add(IROperation(opcode=opcode, inputs=[], outputs=[], attributes={}))

for operation in module.operations:
    print(operation)