NODE_MAPPING = {
    "python": {
        "mapped": {
            # modules
            "Module": "ModuleNode",

            # function definitions
            "arg": "ParameterNode",
            "arguments": "ArgumentsNode",

            # imports
            "Import": "ImportNode",
            "ImportFrom": "ImportNode",
            "alias": "ImportAliasNode",

            # classes and functions
            "ClassDef": "ClassNode",
            "FunctionDef": "FunctionNode",
            "Lambda": "LambdaNode",

            # comprehensions
            "comprehension": "ComprehensionNode",

            # variables
            "Name": "VariableNode",
            "Global": "VariableNode",
            "Nonlocal": "VariableNode",

            # assignments
            "Assign": "AssignmentNode",
            "AnnAssign": "AssignmentNode",
            "AugAssign": "AssignmentNode",
            "NamedExpr": "AssignmentNode",

            # expressions
            "Expr": "ExpressionNode",
            "Attribute": "AttributeNode",
            "Call": "CallNode",
            "Starred": "ExpressionNode",

            # control flow
            "If": "IfNode",
            "For": "ForNode",
            "While": "WhileNode",
            "With": "WithNode",
            "Try": "TryNode",

            # exceptions
            "ExceptHandler": "ExceptNode",
            "Raise": "RaiseNode",
            "Assert": "AssertNode",  # requires an AssertNode

            # calls
            "keyword": "KeywordArgumentNode",

            # with statements
            "withitem": "WithItemNode",

            # returns
            "Return": "ReturnNode",
            "Yield": "YieldNode",  # requires a YieldNode
            "YieldFrom": "YieldFromNode",  # requires a YieldFromNode

            # loop control
            "Break": "BreakNode",
            "Continue": "ContinueNode",
            "Pass": "PassNode",

            # comparisons
            "Compare": "CompareNode",
            "Eq": "CompareNode",
            "Gt": "CompareNode",
            "GtE": "CompareNode",
            "Lt": "CompareNode",
            "LtE": "CompareNode",
            "Is": "CompareNode",
            "IsNot": "CompareNode",
            "In": "CompareNode",
            "NotEq": "CompareNode",
            "NotIn": "CompareNode",

            # boolean operations
            "BoolOp": "BooleanNode",
            "And": "BooleanNode",
            "Or": "BooleanNode",

            # binary operations
            "BinOp": "BinaryOperationNode",
            "Add": "BinaryOperationNode",
            "Sub": "BinaryOperationNode",
            "Mult": "BinaryOperationNode",
            "Div": "BinaryOperationNode",
            "FloorDiv": "BinaryOperationNode",
            "Mod": "BinaryOperationNode",
            "Pow": "BinaryOperationNode",
            "MatMult": "BinaryOperationNode",
            "BitAnd": "BinaryOperationNode",
            "BitOr": "BinaryOperationNode",
            "BitXor": "BinaryOperationNode",

            # unary operations
            "UnaryOp": "UnaryOperationNode",
            "UAdd": "UnaryOperationNode",
            "USub": "UnaryOperationNode",
            "Invert": "UnaryOperationNode",
            "Not": "UnaryOperationNode",

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

            # literals
            "Constant": "LiteralNode",
            "FormattedValue": "FormattedValueNode",  # requires a FormattedValueNode
            "JoinedStr": "FStringNode",  # requires an FStringNode

            # deletion
            "Delete": "DeleteNode",  # requires a DeleteNode
        },

        "unsupported": {

        },
    },
    "cython": {
        "mapped": {

            # modules
            "ModuleNode": "ModuleNode",

            # imports
            "ImportNode": "ImportNode",
            "FromImportStatNode": "ImportNode",

            # classes
            "PyClassDefNode": "ClassNode",
            "CClassDefNode": "ClassNode",

            # functions
            "DefNode": "FunctionNode",
            "CFuncDefNode": "FunctionNode",

            # variables
            "NameNode": "VariableNode",
            "AttributeNode": "AttributeNode",
            "CVarDefNode": "VariableNode",

            # assignments
            "SingleAssignmentNode": "AssignmentNode",
            "InPlaceAssignmentNode": "AssignmentNode",
            "CascadedAssignmentNode": "AssignmentNode",

            # expressions
            "ExprStatNode": "ExpressionNode",
            "TypecastNode": "CastNode",

            # calls
            "SimpleCallNode": "CallNode",
            "GeneralCallNode": "CallNode",

            # control flow
            "IfClauseNode": "IfNode",
            "IfStatNode": "IfNode",
            "ForInStatNode": "ForNode",
            "ForFromStatNode": "ForNode",
            "WhileStatNode": "WhileNode",
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

            # comparisons
            "PrimaryCmpNode": "CompareNode",
            "CascadedCmpNode": "CompareNode",

            # boolean operations
            "BoolBinopNode": "BooleanNode",

            # binary operations
            "AddNode": "BinaryOperationNode",
            "SubNode": "BinaryOperationNode",
            "MulNode": "BinaryOperationNode",
            "DivNode": "BinaryOperationNode",
            "ModNode": "BinaryOperationNode",
            "PowNode": "BinaryOperationNode",
            "IntBinopNode": "BinaryOperationNode",
            "AmpersandNode": "BinaryOperationNode",

            # unary operations
            "NotNode": "UnaryOperationNode",
            "UnaryMinusNode": "UnaryOperationNode",

            # conditional expressions
            "CondExprNode": "ConditionalExpressionNode",

            # collections
            "ListNode": "ListNode",
            "TupleNode": "TupleNode",
            "DictNode": "DictNode",
            "DictItemNode": "DictItemNode",

            # comprehensions
            "ComprehensionNode": "ComprehensionNode",
            "ComprehensionAppendNode": "ComprehensionNode",
            "DictComprehensionAppendNode": "ComprehensionNode",

            # generators
            "GeneratorExpressionNode": "GeneratorNode",
            "IteratorNode": "GeneratorNode",

            # indexing
            "IndexNode": "IndexNode",
            "SliceNode": "SliceNode",
            "SliceIndexNode": "SliceNode",

            # lambdas
            "LambdaNode": "LambdaNode",

            # literals
            "IntNode": "LiteralNode",
            "FloatNode": "LiteralNode",
            "BoolNode": "LiteralNode",
            "NoneNode": "LiteralNode",
            "NullNode": "LiteralNode",
            "BytesNode": "LiteralNode",
            "UnicodeNode": "LiteralNode",
            "IdentifierStringNode": "LiteralNode",
            "FormattedValueNode": "FormattedStringNode",
            "JoinedStrNode": "FormattedStringNode",

            # assertions
            "AssertStatNode": "AssertNode",

            # arrays
            "CythonArrayNode": "ArrayNode",

            # unpacking
            "StarredUnpackingNode": "ExpressionNode",

            # C declarations
            "CStructOrUnionDefNode": "StructNode",
            "CEnumDefNode": "EnumNode",
            "CTypeDefNode": "TypeDefNode",
            "CDefExternNode": "ExternNode",

            # imports
            "CImportStatNode": "ImportNode",
            "FromCImportStatNode": "ImportNode",
        },

        "types": {

            # declarations
            "CArgDeclNode": "ParameterNode",
            "CFuncDeclaratorNode": "FunctionDeclaratorNode",
            "CNameDeclaratorNode": "VariableDeclaratorNode",
            "CEnumDefItemNode": "EnumValueNode",

            # pointers, arrays, references
            "CPtrDeclaratorNode": "PointerNode",
            "CArrayDeclaratorNode": "ArrayDeclaratorNode",
            "CReferenceDeclaratorNode": "ReferenceNode",

            # base types
            "CSimpleBaseTypeNode": "SimpleTypeNode",
            "CComplexBaseTypeNode": "ComplexTypeNode",
            "CConstOrVolatileTypeNode": "QualifiedTypeNode",
            "CNestedBaseTypeNode": "NestedTypeNode",
            "CTupleBaseTypeNode": "TupleTypeNode",

            # advanced types
            "FusedTypeNode": "FusedTypeNode",
            "MemoryViewSliceTypeNode": "MemoryViewTypeNode",
            "TemplatedTypeNode": "TemplatedTypeNode",

            # sizeof
            "SizeofTypeNode": "SizeofTypeNode",
            "SizeofVarNode": "SizeofVariableNode",
        },

        "unsupported": {

            # decorators
            "DecoratorNode": "DecoratorNode",

            # GIL
            "GILStatNode": "GILStatNode",
            "GILExitNode": "GILExitNode",

            # class internals
            "PyClassNamespaceNode": "PyClassNamespaceNode",
            "ClassCellInjectorNode": "ClassCellInjectorNode",

            # statement containers
            "StatListNode": "StatListNode",
        },
    }
}