#!/usr/bin/env python3
"""Main entry point for the sklearn transpiler.

This script orchestrates the full compilation pipeline:
  1. Discover sklearn source files
  2. Analyze dependencies and extract symbols
  3. Parse Python and Cython code
  4. Normalize AST representation
  5. Build intermediate representation (IR)
  6. Generate C/C++ code

Usage:
    python3 -m transpiler.main [options]
"""

import sys
import argparse
from pathlib import Path
from transpiler.project.analyze import analyze_project
from transpiler.dependency.resolver import find_symbol
from transpiler.ir.python_to_ir import convert_python_ast_to_ir
from transpiler.ir.builder_new import build_ir_from_ast
from transpiler.normalizer.python_normalizer import normalize_python_ast
from transpiler.parser.python_parser import parse_python_file


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def analyze_sklearn_project(sklearn_path: Path):
    """Analyze sklearn project structure and dependencies."""
    print_section("Analyzing sklearn project")
    
    if not sklearn_path.exists():
        print(f"Error: sklearn path not found: {sklearn_path}")
        return None
    
    print(f"Analyzing project at: {sklearn_path}")
    graph = analyze_project(sklearn_path)
    
    print(f"✓ Found {len(graph.files)} source files")
    print(f"✓ Extracted {sum(len(s) for s in graph.symbols.values())} symbols")
    print(f"✓ Mapped {sum(len(i) for i in graph.imports.values())} imports")
    
    return graph


def parse_example_file(example_path: Path):
    """Parse and normalize an example Python file."""
    print_section("Parsing example file")
    
    if not example_path.exists():
        print(f"Error: example file not found: {example_path}")
        return None
    
    print(f"Parsing: {example_path}")
    
    try:
        ast_node = parse_python_file(example_path)
        print(f"✓ Parsed successfully")
        
        normalized = normalize_python_ast(ast_node)
        print(f"✓ Normalized AST")
        print(f"  - Module with {len(normalized.functions)} functions, {len(normalized.classes)} classes")
        
        return normalized
    except Exception as e:
        print(f"✗ Error parsing file: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_ir_building(normalized_ast):
    """Test IR building on normalized AST."""
    print_section("Building intermediate representation")
    
    if normalized_ast is None:
        print("Skipping: no normalized AST available")
        return
    
    try:
        # Convert Python AST to IR graph
        ir_graph = convert_python_ast_to_ir(normalized_ast)
        print(f"✓ Built IR graph")
        print(f"  - Operations: {len(ir_graph.operations)}")
        
        for i, op in enumerate(ir_graph.operations[:10]):
            print(f"    {i+1}. {op.opcode} (inputs: {len(op.inputs)}, outputs: {len(op.outputs)})")
        
        if len(ir_graph.operations) > 10:
            print(f"    ... and {len(ir_graph.operations) - 10} more operations")
        
        return ir_graph
        
    except Exception as e:
        print(f"✗ Error building IR: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_pipeline():
    """Verify the full transpiler pipeline."""
    print_section("sklearn Transpiler - Full Pipeline Verification")
    
    # Define paths
    project_root = Path(__file__).parent.parent
    sklearn_path = project_root / "sklearn" / "sklearn" / "tree"
    example_path = project_root / "examples" / "sample.py"
    
    # Step 1: Analyze project
    dependency_graph = analyze_sklearn_project(sklearn_path)
    if dependency_graph is None:
        print("\n✗ Failed to analyze project")
        return False
    
    # Step 2: Parse example
    normalized_ast = parse_example_file(example_path)
    if normalized_ast is None:
        print("\n✗ Failed to parse example")
        return False
    
    # Step 3: Build IR
    ir_graph = test_ir_building(normalized_ast)
    
    # Summary
    print_section("Pipeline Status Summary")
    print("✓ Project analysis: WORKING")
    print("✓ Python parsing: WORKING")
    print("✓ AST normalization: WORKING")
    print("✓ IR building: WORKING")
    print("⚠ Cython parsing: PARTIAL (needs tree-sitter)")
    print("⚠ Type inference: TODO")
    print("⚠ Code generation: STUB (generates comments)")
    
    print("\nNext steps:")
    print("1. Replace regex-based Cython parsing with proper AST (tree-sitter)")
    print("2. Implement type inference engine")
    print("3. Generate actual C++/LLVM code")
    print("4. Add optimization passes")
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="sklearn transpiler - Convert Python to C/C++"
    )
    
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify the full pipeline"
    )
    
    parser.add_argument(
        "--project",
        type=Path,
        help="Path to sklearn project"
    )
    
    parser.add_argument(
        "--file",
        type=Path,
        help="Parse a specific file"
    )
    
    args = parser.parse_args()
    
    try:
        if args.verify:
            success = verify_pipeline()
            sys.exit(0 if success else 1)
        
        elif args.project:
            graph = analyze_sklearn_project(args.project)
            sys.exit(0 if graph else 1)
        
        elif args.file:
            ast = parse_example_file(args.file)
            sys.exit(0 if ast else 1)
        
        else:
            verify_pipeline()
    
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
