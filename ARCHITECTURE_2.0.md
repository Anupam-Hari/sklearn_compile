"""
ARCHITECTURE REDESIGN - sklearn Transpiler 2.0
==============================================

This document describes the new, generalized, production-ready architecture.

GOALS:
1. ✅ Robust Cython parsing that handles any Cython code
2. ✅ Real C++ code generation 
3. ✅ Generalized (non-sklearn-specific)
4. ✅ Future-proof (handles upstream sklearn changes)
5. ✅ Minimal, clean codebase
6. ✅ Easy to extend to new domains (KNN, KMeans, RandomForest, etc.)

CORE PIPELINE:
==============

Source File (.py/.pyx)
    ↓
[Language Detection]
    ↓
[Robust Parser] → Unified AST
    ↓
[Symbol Resolver] → Dependency Graph
    ↓
[Type Inference] → Type Annotations
    ↓
[IR Builder] → Intermediate Representation
    ↓
[C++ Codegen] → Optimized C++ Code
    ↓
Output (.h/.cpp)

KEY CHANGES FROM OLD ARCHITECTURE:
==================================

1. CYTHON PARSING
   OLD: Regex-based (fragile, limited)
   NEW: Token-based parser with proper AST
        - Handles complex Cython constructs
        - Robust to syntax variations
        - Extensible for dialect differences

2. CODE GENERATION
   OLD: Stubs only, sklearn-specific IR operations
   NEW: Real C++ code generation
        - Type-safe code
        - Memory management
        - Optimization-friendly

3. DOMAIN INDEPENDENCE
   OLD: operation_map.py hardcoded sklearn operations
   NEW: Abstract operation handlers
        - Domain plugins
        - Custom type mapping
        - Extensible operation set

4. TYPE SYSTEM
   OLD: None
   NEW: Basic type inference
        - Variable tracking
        - Function signatures
        - Type propagation

5. CODEBASE SIZE
   OLD: 3138 lines (includes redundant code)
   NEW: ~1500 lines (focused, minimal)

FILES TO KEEP:
==============
transpiler/
├── ast/
│   ├── __init__.py
│   └── nodes.py              # Unified AST definitions
├── parser/
│   ├── __init__.py
│   ├── python_parser.py      # Python parsing
│   └── cython_parser.py      # NEW: Robust Cython parser (token-based)
├── normalizer/
│   ├── __init__.py
│   ├── python_normalizer.py
│   ├── cython_normalizer.py
│   └── generic_normalizer.py # NEW: Generic normalizer
├── ir/
│   ├── __init__.py
│   ├── models.py             # IR definitions (domain-agnostic)
│   ├── graph.py              # IR graph
│   ├── builder.py            # Generic IR builder
│   └── python_to_ir.py
├── codegen/
│   ├── __init__.py
│   ├── cpp_generator.py      # NEW: Real C++ generator
│   └── type_mapper.py        # NEW: Type mapping
├── dependency/
│   ├── __init__.py
│   ├── models.py             # Symbol, DependencyGraph
│   ├── resolver.py           # Find symbols
│   └── extractor.py          # Extract imports/symbols
├── type_inference/
│   ├── __init__.py
│   └── engine.py             # NEW: Type inference
├── project/
│   ├── __init__.py
│   └── analyze.py            # Project discovery
├── cli/
│   ├── __init__.py
│   └── cli.py                # CLI interface
├── __init__.py
├── __main__.py
├── main.py                   # Pipeline verification
└── README.md

FILES TO DELETE:
================
transpiler/cython/            # All (replace with proper parser)
transpiler/cli/discover.py, extract_*.py, etc.  # Unused
transpiler/dependency/dependency_graph.py       # Old
transpiler/dependency/classifier.py             # sklearn-specific
transpiler/symbols/                             # Redundant
transpiler/type_inference/                      # Will replace
transpiler/pipeline/                            # Examples only
transpiler/graph/recursive_walker.py            # Unused
transpiler/normalizer/cython_normalizer.py      # Will replace

FILES TO CREATE:
================
transpiler/parser/cython_parser.py      # NEW: Proper tokenizer-based parser
transpiler/codegen/cpp_generator.py     # NEW: Real C++ code generation
transpiler/type_inference/engine.py     # NEW: Type inference
transpiler/ir/builder.py                # ENHANCE: Make domain-agnostic
transpiler/normalizer/generic_normalizer.py  # NEW: Generic normalizer

STRATEGY FOR ROBUSTNESS:
=======================

1. Cython Parser:
   - Tokenize input first (not regex)
   - Build proper AST with all node types
   - Handle all Cython constructs (cdef, cpdef, cimport, etc.)
   - Handle syntax edge cases
   - Recoverable error handling

2. Type Inference:
   - Track variable assignments
   - Propagate types through operations
   - Handle type aliases and typedef
   - Support Cython type annotations (int, double, etc.)

3. C++ Codegen:
   - One-to-one mapping from IR to C++
   - Handle memory management
   - Generate proper headers
   - Support both C++11 and C++17

4. Extensibility:
   - Plugin system for domain-specific types
   - Custom type mappings per domain
   - Operation handlers registry
   - Template-based code generation

UPGRADING ON sklearn CHANGES:
=============================

If sklearn tree module changes:
  1. Re-run transpiler on new tree module
  2. Symbol resolver automatically finds new symbols
  3. Parser handles new syntax automatically
  4. Type inference recomputes types
  5. Codegen produces updated C++
  
No architecture changes needed!

If sklearn changes:
  1. Update domain plugin if needed
  2. Re-parse and re-generate
  3. All else automatic

If you add KNN/KMeans/RandomForest:
  1. Create new domain module in transpiler/domains/
  2. Register custom types and operations
  3. Point transpiler at new code
  4. Generate C++ automatically
"""

if __name__ == "__main__":
    print(__doc__)
