PYTHON_EXPRESSIONS = {
    "Call": "CallExpressionNode",
    "Constant": "ConstantNode",
    "List": "ListExpressionNode",
    "Tuple": "TupleExpressionNode",
    "Dict": "DictExpressionNode",
    "Set": "SetExpressionNode",
    "ListComp": "ListComprehensionNode",
    "DictComp": "DictComprehensionNode",
    "SetComp": "SetComprehensionNode",
    "GeneratorExp": "GeneratorExpressionNode",
    "Lambda": "LambdaExpressionNode",
    "Slice": "SliceExpressionNode",
    "IfExp": "ConditionalExpressionNode",
    "Yield": "YieldExpressionNode",
    "YieldFrom": "YieldFromExpressionNode",
    "JoinedStr": "FStringNode",
    "FormattedValue": "FormattedValueNode",
    "Starred": "StarredExpressionNode",
    "comprehension": "ComprehensionNode",
}

CYTHON_EXPRESSIONS = {

    "IntNode": "IntegerLiteralNode",

    "FloatNode": "FloatLiteralNode",

    "BoolNode": "BooleanLiteralNode",

    "UnicodeNode": "StringLiteralNode",

    "BytesNode": "BytesLiteralNode",

    "IdentifierStringNode": "IdentifierLiteralNode",

    "NoneNode": "NoneLiteralNode",

    "NullNode": "NullLiteralNode",

    "ListNode": "ListExpressionNode",

    "TupleNode": "TupleExpressionNode",

    "DictNode": "DictionaryExpressionNode",

    "DictItemNode": "DictionaryItemNode",

    "SliceNode": "SliceExpressionNode",

    "SimpleCallNode": "CallExpressionNode",

    "GeneralCallNode": "CallExpressionNode",

    "LambdaNode": "LambdaExpressionNode",

    "CondExprNode": "ConditionalExpressionNode",

    "YieldExprNode": "YieldExpressionNode",

    "JoinedStrNode": "FStringNode",

    "FormattedValueNode": "FormattedValueNode",

    "ComprehensionNode": "ComprehensionNode",

    "ComprehensionAppendNode": "ComprehensionAppendNode",

    "DictComprehensionAppendNode": "DictionaryComprehensionAppendNode",

    "GeneratorExpressionNode": "GeneratorExpressionNode",

    "StarredUnpackingNode": "StarredUnpackingNode",

    "TypecastNode": "TypeCastNode",

    "SizeofVarNode": "SizeofVariableNode",

    "SizeofTypeNode": "SizeofTypeNode",

    "CythonArrayNode": "ArrayExpressionNode",

}