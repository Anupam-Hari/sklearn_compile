# sklearn Transpiler

Convert Python/Cython code to optimized C/C++ implementations.

## Architecture

The transpiler follows a classic compiler pipeline:

```
Source Discovery
    ↓
Project Analysis (find files, extract symbols)
    ↓
Parsing (Python AST | Cython regex-based)
    ↓
Normalization (unified AST representation)
    ↓
IR Building (intermediate representation)
    ↓
Type Inference (resolve types)
    ↓
Code Generation (C/C++/LLVM)
```

## Module Organization

```
transpiler/
├── main.py                 # Main pipeline verification
├── __main__.py            # CLI entry point
├── cli/                   # Command-line interface
│   ├── cli.py            # Main CLI subcommands
│   ├── analyze.py        # Analyze command
│   ├── parse.py          # Parse command
│   └── extract_*.py      # Extraction utilities
├── ast/                   # Normalized AST nodes
│   └── nodes.py          # FunctionNode, ClassNode, etc.
├── parser/               # Source code parsing
│   ├── python_parser.py # Python AST parsing
│   └── cython_parser.py # Cython parsing (regex-based)
├── normalizer/           # AST normalization
│   ├── python_normalizer.py
│   └── cython_normalizer.py
├── ir/                   # Intermediate representation
│   ├── models.py         # IROperation, IRGraph
│   ├── graph.py          # IRGraph implementation
│   ├── builder.py        # sklearn-specific IR builders
│   ├── ir_builder.py     # Cython to IR converter
│   ├── control.py        # Control flow operations
│   └── python_to_ir.py   # Python ModuleNode to IR converter
├── dependency/           # Dependency analysis
│   ├── models.py         # Symbol, DependencyGraph
│   ├── resolver.py       # Find symbols
│   ├── extractor.py      # Extract imports/symbols
│   └── method_calls.py   # Analyze method calls
├── cython/               # Cython-specific processing
│   ├── nodes.py          # CythonNode tree types
│   ├── block_parser.py   # Indentation-based block parsing
│   ├── ir_builder.py     # CythonNode to IR converter
│   ├── statement_parser.py # Wrapper for parsing
│   ├── method_extractor.py # Extract method source
│   ├── operation_map.py   # Call to operation mapping
│   └── calls.py          # Extract function calls
├── project/             # Project structure analysis
│   ├── analyze.py       # Project analysis entry point
│   └── index.py         # Build project index
├── graph/               # Graph algorithms
│   ├── walker.py        # Tree traversal
│   └── recursive_walker.py
├── symbols/             # Symbol table management
│   └── extractor.py
├── type_inference/      # Type analysis (empty - TODO)
└── pipeline/            # Example pipelines
    └── dependency_pipeline.py
```

## Quick Start

### Verify the Pipeline

```bash
python3 -m transpiler verify
```

### Parse a File

```bash
python3 -m transpiler parse examples/sample.py
python3 -m transpiler parse examples/sample.py --format tree
```

### Build IR

```bash
python3 -m transpiler build-ir examples/sample.py
```

### Analyze a Project

```bash
python3 -m transpiler analyze sklearn/sklearn/tree
```

## Current Status

✅ **Complete**
- Project analysis and file discovery
- Python parsing and normalization
- AST representation
- Dependency graph building
- Symbol extraction
- Basic IR building for Python code

⚠️ **Partial**
- Cython parsing (uses regex, needs tree-sitter)
- IR building for Cython (basic)

❌ **Not Implemented**
- Type inference engine
- Code generation (C/C++)
- Optimization passes
- Cross-module type tracking

## Next Steps

1. **Replace Cython parsing** with proper AST using tree-sitter
2. **Implement type inference** engine
3. **Generate actual C++** code instead of stubs
4. **Add optimization passes** (constant folding, dead code elimination, etc.)
5. **Support LLVM backend** for further optimizations

## Development

The codebase is organized to make it easy to:
- Add new AST node types
- Implement new IR operations
- Add parsing support for other languages
- Extend with new analysis passes

All modules follow clean architecture principles with clear separation of concerns.
