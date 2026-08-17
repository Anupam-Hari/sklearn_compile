PYTHON_TO_NORMALIZED = {
    # modules
    "Module": "ModuleNode",

    # imports
    "Import": "ImportNode",
    "ImportFrom": "ImportNode",

    # symbols
    "ClassDef": "ClassNode",
    "FunctionDef": "FunctionNode",

    # variables
    "Name": "VariableNode",

    # assignments
    "Assign": "AssignmentNode",
    "AnnAssign": "AssignmentNode",
    "AugAssign": "AssignmentNode",

    # expressions
    "Expr": "ExpressionNode",
    "Call": "CallNode",
    "Attribute": "AttributeNode",

    # control flow
    "If": "IfNode",
    "For": "ForNode",
    "While": "WhileNode",
    "With": "WithNode",
    "Try": "TryNode",
    "ExceptHandler": "ExceptNode",

    # returns
    "Return": "ReturnNode",
    "Raise": "RaiseNode",

    # loop control
    "Break": "BreakNode",
    "Continue": "ContinueNode",
    "Pass": "PassNode",

    # comparisons and operations
    "Compare": "CompareNode",
    "BoolOp": "BooleanNode",
    "BinOp": "BinaryOperationNode",
    "UnaryOp": "UnaryOperationNode",

    # conditional expressions
    "IfExp": "ConditionalExpressionNode",

    # collections
    "List": "ListNode",
    "Tuple": "TupleNode",
    "Dict": "DictNode",
    "Set": "SetNode",

    # comprehensions
    "ListComp": "ListComprehensionNode",
    "DictComp": "DictComprehensionNode",
    "SetComp": "SetComprehensionNode",
    "GeneratorExp": "GeneratorNode",

    # indexing
    "Subscript": "IndexNode",
    "Slice": "SliceNode",

    # functions
    "Lambda": "LambdaNode",

    # strings
    "FormattedValue": "FormattedValueNode",
    "JoinedStr": "FStringNode",

    # generators
    "Yield": "YieldNode",
    "YieldFrom": "YieldFromNode",

    # newer Python features
    "NamedExpr": "WalrusNode",

    # declarations
    "Global": "GlobalNode",
    "Nonlocal": "NonlocalNode",

    # unpacking
    "Starred": "StarredNode",

    # deletion
    "Delete": "DeleteNode",
}

PYTHON_OPERATORS = {
    # arithmetic
    "Add",
    "Sub",
    "Mult",
    "Div",
    "FloorDiv",
    "Mod",
    "Pow",
    "MatMult",

    # comparison
    "Eq",
    "NotEq",
    "Lt",
    "LtE",
    "Gt",
    "GtE",
    "Is",
    "IsNot",
    "In",
    "NotIn",

    # boolean
    "And",
    "Or",
    "Not",

    # unary
    "USub",
    "UAdd",
    "Invert",

    # bitwise
    "BitAnd",
    "BitOr",
    "BitXor",
    "LShift",
}

CYTHON_TO_NORMALIZED = {
    # modules
    "ModuleNode": "ModuleNode",

    # imports
    "ImportNode": "ImportNode",
    "FromImportStatNode": "ImportNode",
    "CImportStatNode": "ImportNode",
    "FromCImportStatNode": "ImportNode",

    # symbols
    "CClassDefNode": "ClassNode",
    "PyClassDefNode": "ClassNode",
    "Py3ClassNode": "ClassNode",
    "DefNode": "FunctionNode",
    "CFuncDefNode": "FunctionNode",
    "LambdaNode": "FunctionNode",
    "CStructOrUnionDefNode": "StructNode",
    "CEnumDefNode": "EnumNode",
    "CDefExternNode": "ExternNode",
    "CTypeDefNode": "TypeDefNode",

    # variables
    "CVarDefNode": "VariableNode",
    "NameNode": "VariableNode",
    "AttributeNode": "AttributeNode",
    "CArgDeclNode": "ParameterNode",
    "CNameDeclaratorNode": "VariableNode",

    # assignments
    "SingleAssignmentNode": "AssignmentNode",
    "CascadedAssignmentNode": "AssignmentNode",
    "InPlaceAssignmentNode": "AssignmentNode",

    # calls
    "SimpleCallNode": "CallNode",
    "GeneralCallNode": "CallNode",

    # control flow
    "IfStatNode": "IfNode",
    "ForInStatNode": "ForNode",
    "WhileStatNode": "WhileNode",
    "ForFromStatNode": "ForNode",
    "WithStatNode": "WithNode",
    "TryExceptStatNode": "TryNode",
    "ExceptClauseNode": "ExceptNode",

    # returns
    "ReturnStatNode": "ReturnNode",
    "YieldExprNode": "YieldNode",

    # loop control
    "BreakStatNode": "BreakNode",
    "ContinueStatNode": "ContinueNode",
    "PassStatNode": "PassNode",

    # declarations
    "MemoryViewSliceTypeNode": "MemoryViewNode",
    "CPtrDeclaratorNode": "PointerNode",
    "CArrayDeclaratorNode": "ArrayNode",
    "CReferenceDeclaratorNode": "ReferenceNode",

    "ListNode": "ListNode",
    "TupleNode": "TupleNode",
    "DictNode": "DictNode",
    "DictItemNode": "DictItemNode",
    "IndexNode": "IndexNode",
    "SliceNode": "SliceNode",
    "SliceIndexNode": "SliceNode",
    "CondExprNode": "ConditionalExpressionNode",
    "NotNode": "UnaryOperationNode",
    "UnaryMinusNode": "UnaryOperationNode",
    "TypecastNode": "CastNode",
    "SizeofTypeNode": "SizeofNode",
    "SizeofVarNode": "SizeofNode",
    "CythonArrayNode": "ArrayNode",
    "IntNode": "LiteralNode",
    "FloatNode": "LiteralNode",
    "BoolNode": "LiteralNode",
    "NoneNode": "LiteralNode",
    "UnicodeNode": "LiteralNode",
    "BytesNode": "LiteralNode",
    "BytesLiteral": "LiteralNode",
    "FormattedValueNode": "FormattedStringNode",
    "JoinedStrNode": "FormattedStringNode",
    "IdentifierStringNode": "LiteralNode",
    "ComprehensionNode": "ComprehensionNode",
    "ComprehensionAppendNode": "ComprehensionNode",
    "DictComprehensionAppendNode": "ComprehensionNode",
    "GeneratorExpressionNode": "GeneratorExpressionNode",
    "PrimaryCmpNode": "CompareNode",
    "CascadedCmpNode": "CompareNode",
    "AddNode": "BinaryOperationNode",
    "SubNode": "BinaryOperationNode",
    "MulNode": "BinaryOperationNode",
    "DivNode": "BinaryOperationNode",
    "ModNode": "BinaryOperationNode",
    "PowNode": "BinaryOperationNode",
    "IntBinopNode": "BinaryOperationNode",
    "AmpersandNode": "BinaryOperationNode",
    "BoolBinopNode": "BooleanNode",
    "RaiseStatNode": "RaiseNode",
    "AssertStatNode": "AssertNode",
    "ExprStatNode": "ExpressionNode",
}