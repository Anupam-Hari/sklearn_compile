PYTHON_OPERATIONS = {
    "BinOp": "BinaryOperationNode",
    "UnaryOp": "UnaryOperationNode",
    "BoolOp": "BooleanOperationNode",
    "Compare": "ComparisonOperationNode",
    "AugAssign": "AugmentedAssignmentNode",

    "Add": "AddOperationNode",
    "Sub": "SubtractOperationNode",
    "Mult": "MultiplyOperationNode",
    "Div": "DivideOperationNode",
    "FloorDiv": "FloorDivideOperationNode",
    "Mod": "ModuloOperationNode",
    "Pow": "PowerOperationNode",
    "MatMult": "MatrixMultiplyOperationNode",

    "BitOr": "BitwiseOrOperationNode",
    "BitAnd": "BitwiseAndOperationNode",
    "BitXor": "BitwiseXorOperationNode",
    "LShift": "LeftShiftOperationNode",

    "And": "LogicalAndOperationNode",
    "Or": "LogicalOrOperationNode",

    "USub": "UnaryMinusOperationNode",
    "UAdd": "UnaryPlusOperationNode",
    "Not": "LogicalNotOperationNode",
    "Invert": "BitwiseInvertOperationNode",

    "Eq": "EqualOperationNode",
    "NotEq": "NotEqualOperationNode",
    "Lt": "LessThanOperationNode",
    "LtE": "LessThanOrEqualOperationNode",
    "Gt": "GreaterThanOperationNode",
    "GtE": "GreaterThanOrEqualOperationNode",
    "Is": "IdentityOperationNode",
    "IsNot": "NotIdentityOperationNode",
    "In": "MembershipOperationNode",
    "NotIn": "NotMembershipOperationNode",
}

CYTHON_OPERATIONS = {

    "AddNode": "AddOperationNode",

    "SubNode": "SubtractOperationNode",

    "MulNode": "MultiplyOperationNode",

    "DivNode": "DivideOperationNode",

    "ModNode": "ModuloOperationNode",

    "PowNode": "PowerOperationNode",

    "IntBinopNode": "IntegerBinaryOperationNode",

    "BoolBinopNode": "BooleanOperationNode",

    "PrimaryCmpNode": "ComparisonOperationNode",

    "CascadedCmpNode": "CascadedComparisonNode",

    "UnaryMinusNode": "UnaryMinusOperationNode",

    "NotNode": "LogicalNotOperationNode",

    "AmpersandNode": "AddressOfOperationNode",

}