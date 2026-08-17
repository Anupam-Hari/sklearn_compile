UNSUPPORTED_CYTHON_NODES = {
    # decorators
    "DecoratorNode",

    # exceptions
    "RaiseStatNode",

    # comprehensions
    "ComprehensionNode",
    "DictComprehensionAppendNode",
    "StarredUnpackingNode",

    # generators
    "GeneratorExpressionNode",

    # fused types
    "FusedType",
    "FusedTypeNode",

    # f-strings
    "JoinedStrNode",
    "FormattedValueNode",

    # unsupported language features
    "AssertStatNode",
}

UNSUPPORTED_PYTHON_NODES = {
    "GeneratorExp",
    "ListComp",
    "comprehension",
    "Try",
    "With",
    "Raise",
    "JoinedStr",
    "FormattedValue",
    "NamedExpr",
    "Starred",
}