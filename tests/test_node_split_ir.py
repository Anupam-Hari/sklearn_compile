from transpiler.ir.models import IRModule, IROperation


graph = IRModule()

graph.add(IROperation(opcode="BeginLoop", inputs=[], outputs=[], attributes={"type": "candidate_features"}))
graph.add(IROperation(opcode="ExtractFeatureColumn", inputs=[], outputs=[], attributes={"index": 0}))
graph.add(IROperation(opcode="SortSamples", inputs=[], outputs=[], attributes={}))
graph.add(IROperation(opcode="BeginLoop", inputs=[], outputs=[], attributes={"type": "candidate_thresholds"}))
graph.add(IROperation(opcode="EvaluateSplit", inputs=[], outputs=[], attributes={}))
graph.add(IROperation(opcode="Branch", inputs=[], outputs=[], attributes={"condition": "improvement > best"}))
graph.add(IROperation(opcode="EndLoop", inputs=[], outputs=[], attributes={"type": "candidate_thresholds"}))
graph.add(IROperation(opcode="PartitionSamples", inputs=[], outputs=[], attributes={}))
graph.add(IROperation(opcode="CreateNode", inputs=[], outputs=[], attributes={}))
graph.add(IROperation(opcode="EndLoop", inputs=[], outputs=[], attributes={"type": "candidate_features"}))
graph.add(IROperation(opcode="Return", inputs=[], outputs=[], attributes={"value": "best_split"}))

for op in graph.operations:
    print(op)