from transpiler.ir.models import IRModule


OPCODE_MAP = {
    "ExtractFeatureColumn": "// extract feature column",
    "SortSamples": "// sort samples",
    "EvaluateSplit": "// evaluate split",
    "PartitionSamples": "// partition samples",
    "CreateNode": "// create tree node",
}


def generate_cpp(ir_module: IRModule) -> str:
    lines = []

    for operation in ir_module.operations:
        lines.append(OPCODE_MAP.get(operation.opcode, "// unknown"))

    return "\n".join(lines)