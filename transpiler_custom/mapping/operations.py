PYTHON_OPERATIONS = {

    "BinOp": "BinaryOperationNode",

    "BoolOp": "BooleanOperationNode",

    "UnaryOp": "UnaryOperationNode",

    "Compare": "ComparisonNode",

}

CYTHON_OPERATIONS = {

    "AddNode": "BinaryOperationNode",
    "SubNode": "BinaryOperationNode",
    "MulNode": "BinaryOperationNode",
    "DivNode": "BinaryOperationNode",
    "ModNode": "BinaryOperationNode",
    "PowNode": "BinaryOperationNode",

    "AmpersandNode": "BinaryOperationNode",

    "BoolBinopNode": "BooleanOperationNode",

    "IntBinopNode": "BinaryOperationNode",

    "PrimaryCmpNode": "ComparisonNode",
    "CascadedCmpNode": "ComparisonNode",

    "NotNode": "UnaryOperationNode",

    "UnaryMinusNode": "UnaryOperationNode",

}