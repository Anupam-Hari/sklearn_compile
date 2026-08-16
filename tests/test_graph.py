from transpiler.ir.models import IRModule, IROperation


graph = IRModule()

for opcode in [
    "ExtractFeatureColumn",
    "SortSamples",
    "EvaluateSplit",
    "PartitionSamples",
    "CreateNode",
]:
    graph.add(IROperation(opcode=opcode, inputs=[], outputs=[], attributes={}))

graph.operations