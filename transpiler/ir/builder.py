from transpiler.ir.models import IROperation


def extract_feature_column(feature_index: int) -> IROperation:
    return IROperation(
        opcode="ExtractFeatureColumn",
        inputs=["X", "samples"],
        outputs=["feature_values"],
        attributes={
            "feature_index": feature_index,
        },
    )


def sort_samples() -> IROperation:
    return IROperation(
        opcode="SortSamples",
        inputs=["feature_values", "samples"],
        outputs=["feature_values", "samples"],
    )


def evaluate_split() -> IROperation:
    return IROperation(
        opcode="EvaluateSplit",
        inputs=["feature_values", "samples"],
        outputs=["SplitRecord"],
    )


def partition_samples() -> IROperation:
    return IROperation(
        opcode="PartitionSamples",
        inputs=["samples", "SplitRecord"],
        outputs=["samples"],
    )


def create_node() -> IROperation:
    return IROperation(
        opcode="CreateNode",
        inputs=["ParentInfo", "SplitRecord"],
        outputs=["Node"],
    )