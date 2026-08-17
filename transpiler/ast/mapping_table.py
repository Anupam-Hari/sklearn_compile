PYTHON_TO_NORMALIZED = {
    "Module": "ModuleNode",
    "Import": "ImportNode",
    "ImportFrom": "ImportNode",
    "ClassDef": "ClassNode",
    "FunctionDef": "FunctionNode",
    "Assign": "AssignmentNode",
    "AnnAssign": "AssignmentNode",
    "AugAssign": "AssignmentNode",
    "Return": "ReturnNode",
    "Call": "CallNode",
    "If": "IfNode",
    "For": "ForNode",
    "While": "WhileNode",
    "Attribute": "AttributeNode",
    "Name": "VariableNode",
    "Subscript": "IndexNode",
    "Compare": "CompareNode",
    "BoolOp": "BooleanNode",
    "BinOp": "BinaryOperationNode",
    "IfExp": "ConditionalExpressionNode",
    "List": "ListNode",
    "Tuple": "TupleNode",
    "Dict": "DictNode",
    "Set": "SetNode",
    "Slice": "SliceNode",
    "Break": "BreakNode",
    "Continue": "ContinueNode",
}

PYTHON_OPERATORS = {
    "Add",
    "Sub",
    "Mult",
    "Div",
    "Mod",
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
    "And",
    "Or",
    "Not",
    "USub",
    "Invert",
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
    "DefNode": "FunctionNode",
    "CFuncDefNode": "FunctionNode",
    "CStructOrUnionDefNode": "StructNode",
    "CEnumDefNode": "EnumNode",
    "CDefExternNode": "ExternNode",

    # variables
    "CVarDefNode": "VariableNode",
    "NameNode": "VariableNode",
    "AttributeNode": "VariableNode",

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

    # returns
    "ReturnStatNode": "ReturnNode",

    # loop control
    "BreakStatNode": "BreakNode",
    "ContinueStatNode": "ContinueNode",

    # declarations
    "MemoryViewSliceTypeNode": "MemoryViewNode",
    "CPtrDeclaratorNode": "PointerNode",
    "CArrayDeclaratorNode": "ArrayNode",
    "CReferenceDeclaratorNode": "ReferenceNode",
}