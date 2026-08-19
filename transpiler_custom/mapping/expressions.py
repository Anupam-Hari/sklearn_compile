PYTHON_EXPRESSIONS = {

    "Call": "CallNode",

    "Attribute": "AttributeNode",

    "Name": "NameNode",

    "Subscript": "SubscriptNode",

    "Lambda": "LambdaNode",

    "Dict": "DictNode",

    "List": "ListNode",

    "Tuple": "TupleNode",

    "Set": "SetNode",

    "GeneratorExp": "GeneratorExpressionNode",

    "ListComp": "ListComprehensionNode",

    "DictComp": "DictComprehensionNode",

    "SetComp": "SetComprehensionNode",

}

CYTHON_EXPRESSIONS = {

    "AttributeNode": "AttributeNode",

    "NameNode": "NameNode",

    "GeneralCallNode": "CallNode",
    "SimpleCallNode": "CallNode",

    "LambdaNode": "LambdaNode",

    "DictNode": "DictNode",
    "ListNode": "ListNode",
    "TupleNode": "TupleNode",

    "GeneratorExpressionNode": "GeneratorExpressionNode",

    "ComprehensionNode": "ComprehensionNode",

    "IndexNode": "IndexNode",
    "SliceNode": "SliceNode",
    "SliceIndexNode": "SliceNode",

    "CondExprNode": "ConditionalExpressionNode",

    "TypecastNode": "TypeCastNode",

    "SizeofTypeNode": "SizeofNode",
    "SizeofVarNode": "SizeofNode",

    "CythonArrayNode": "ArrayNode",

}