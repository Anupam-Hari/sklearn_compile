#!/usr/bin/env python3
"""
Quick start guide for the sklearn transpiler.

Run this script to get started with the transpiler and verify everything works.
"""

import sys
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def run_verification():
    """Run the full pipeline verification."""
    from transpiler.main import verify_pipeline
    
    print_header("Running Pipeline Verification")
    success = verify_pipeline()
    return success


def show_examples():
    """Show usage examples."""
    print_header("Usage Examples")
    
    examples = [
        ("Verify pipeline", "python3 -m transpiler verify"),
        ("Parse file", "python3 -m transpiler parse examples/sample.py"),
        ("View parsed AST", "python3 -m transpiler parse examples/sample.py --format tree"),
        ("Build IR", "python3 -m transpiler build-ir examples/sample.py"),
        ("Analyze project", "python3 -m transpiler analyze sklearn/sklearn/tree"),
        ("Run tests", "python3 test_transpiler.py"),
    ]
    
    for title, cmd in examples:
        print(f"{title}:")
        print(f"  $ {cmd}\n")


def show_next_steps():
    """Show next steps for development."""
    print_header("Next Development Steps")
    
    steps = [
        "1. Enhanced Cython Parsing",
        "   Replace regex-based parsing with proper AST using tree-sitter",
        "   Location: transpiler/cython/improved_parser.py",
        "   Impact: Better handling of complex Cython syntax",
        "",
        "2. Type Inference Engine",
        "   Implement flow-sensitive type analysis",
        "   Location: transpiler/type_inference/",
        "   Impact: Enable type-aware optimizations",
        "",
        "3. Code Generation",
        "   Generate actual C++/LLVM code",
        "   Location: transpiler/codegen/",
        "   Impact: Complete compiler pipeline",
        "",
        "4. Optimization Passes",
        "   Add peephole and global optimizations",
        "   Location: transpiler/optimizer/",
        "   Impact: Better performance of generated code",
        "",
        "5. Testing & Documentation",
        "   Expand test coverage and add integration tests",
        "   Location: tests/ and documentation/",
        "   Impact: Production-ready transpiler",
    ]
    
    for step in steps:
        print(step)


def show_architecture():
    """Show the transpiler architecture."""
    print_header("Transpiler Architecture")
    
    print("""
The transpiler follows a classic compiler pipeline:

    Source Files (.py, .pyx)
            ↓
    Project Discovery & Analysis
            ↓
    Language-Specific Parsing
            ↓
    AST Normalization
            ↓
    Intermediate Representation Building
            ↓
    Type Inference (TODO)
            ↓
    Code Generation (TODO)
            ↓
    Optimized C/C++ Output

Key Components:
- parser/: Parse Python and Cython source files
- normalizer/: Convert to unified AST
- ir/: Build intermediate representation
- dependency/: Analyze dependencies and symbols
- cython/: Cython-specific processing
- cli/: Command-line interface
""")


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("  sklearn Transpiler - Quick Start Guide")
    print("=" * 70)
    
    # Show what this is
    print("""
This transpiler converts Python/Cython code to optimized C/C++ implementations.

Current Status: ✅ Core pipeline working

Core Functionality:
  ✓ Project analysis and symbol extraction
  ✓ Python file parsing and normalization
  ✓ Dependency graph building
  ✓ Intermediate representation generation
  ✓ Full command-line interface

TODO:
  • Type inference engine
  • Real C/C++ code generation
  • Optimization passes
""")
    
    # Run verification
    try:
        success = run_verification()
        if not success:
            print("\n✗ Pipeline verification failed")
            return 1
    except Exception as e:
        print(f"\n✗ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Show usage examples
    show_examples()
    
    # Show architecture
    show_architecture()
    
    # Show next steps
    show_next_steps()
    
    print_header("Getting Started")
    print("""
Quick start commands:

  1. Verify the pipeline works:
     python3 -m transpiler verify

  2. Parse a Python file:
     python3 -m transpiler parse examples/sample.py --format tree

  3. Run the test suite:
     python3 test_transpiler.py

  4. Analyze sklearn project:
     python3 -m transpiler analyze sklearn/sklearn/tree

For more help:
  python3 -m transpiler --help
  python3 -m transpiler <command> --help
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
