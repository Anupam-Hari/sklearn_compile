CYTHON_TYPES = {
    # primitive C types
    "CSimpleBaseTypeNode": "primitive",

    # pointers
    "CPtrDeclaratorNode": "pointer",
    "CPtrType": "pointer",

    # arrays
    "CArrayDeclaratorNode": "array",

    # references
    "CReferenceDeclaratorNode": "reference",

    # memoryviews
    "MemoryViewSliceTypeNode": "memoryview",

    # structs
    "CStructOrUnionDefNode": "struct",
    "CStructOrUnionType": "struct",

    # enums
    "CEnumDefNode": "enum",

    # typedefs
    "CTypedefType": "typedef",

    # function signatures
    "CFuncType": "function_type",
    "CFuncTypeArg": "parameter",

    # qualifiers
    "CConstOrVolatileTypeNode": "qualified_type",
}