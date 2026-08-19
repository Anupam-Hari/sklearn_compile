PYTHON_SYMBOLS = {

    "Module": "ModuleNode",

    "ClassDef": "ClassNode",

    "FunctionDef": "FunctionNode",

    # "Assign": "AssignmentNode",

    # "AnnAssign": "AssignmentNode",

}

CYTHON_SYMBOLS = {

    # module
    "ModuleNode": "ModuleNode",

    # Python-style definitions
    "DefNode": "FunctionNode",
    "PyClassDefNode": "ClassNode",

    # Cython/C definitions
    "CFuncDefNode": "FunctionNode",
    "CClassDefNode": "ClassNode",

    "CVarDefNode": "VariableNode",

    "CTypeDefNode": "TypeDefinitionNode",

    "CStructOrUnionDefNode": "StructNode",

    "CEnumDefNode": "EnumNode",

    "CDefExternNode": "ExternBlockNode",

}