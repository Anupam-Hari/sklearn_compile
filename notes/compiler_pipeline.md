Compiler pipeline

Phase 1: Source discovery

Input:

    sklearn/

Output:

    source file list

--------------------------------------------------

Phase 2: Dependency extraction

Input:

    source file

Output:

    dependency graph

--------------------------------------------------

Phase 3: Parsing

Input:

    .py
    .pyx
    .pxd
    .pxi

Output:

    raw AST

--------------------------------------------------

Phase 4: AST normalization

Convert language-specific constructs into a common representation.

Examples:

    Python classes

    Cython cdef classes

    Python functions

    Cython cdef functions

    Python loops

    Cython loops

Output:

    normalized AST

--------------------------------------------------

Phase 5: Type inference

Infer:

    int

    float

    bool

    pointers

    arrays

    memory views

Output:

    typed AST

--------------------------------------------------

Phase 6: Kernel extraction

Extract computational kernels.

Examples:

    TreeBuilder

    Splitter

    Partitioner

    Criterion

Output:

    kernel graph

--------------------------------------------------

Phase 7: IR generation

Convert kernels into IR nodes.

Output:

    ForestIR

    TreeBuilderIR

    SplitterIR

    PartitionerIR

    CriterionIR

--------------------------------------------------

Phase 8: Code generation

IR

↓

C++

Output:

    .hpp

    .cpp

--------------------------------------------------

Phase 9: Runtime linking

Link generated code against:

    runtime/common

    runtime/tree

    runtime/criterion

    runtime/partitioner

    runtime/forest

--------------------------------------------------

Phase 10: Validation

Compare:

    sklearn output

vs

    generated C++ output