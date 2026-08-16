"""
New transpiler pipeline - From source to C++ code.

This is the main orchestration for the refactored transpiler.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any


def transpile_python_to_cpp(source_path: Path, output_path: Optional[Path] = None,
                           namespace: str = "sklearn") -> str:
    """
    Transpile Python/Cython source to C++ code.
    
    Args:
        source_path: Path to Python/Cython file
        output_path: Optional path to write C++ output
        namespace: C++ namespace for generated code
    
    Returns:
        Generated C++ code as string
    """
    from transpiler.parser.python_parser import parse_python_file
    from transpiler.parser.cython_parser import parse_cython_file
    from transpiler.normalizer.python_normalizer import normalize_python_ast
    from transpiler.ir.builder_new import build_ir_from_ast
    from transpiler.codegen.cpp_generator_new import generate_cpp_from_ir, CppConfig
    from transpiler.type_inference.engine import TypeInferenceEngine
    
    # Read source
    source_code = source_path.read_text()
    
    # Detect language
    is_cython = source_path.suffix == '.pyx'
    language = 'cython' if is_cython else 'python'
    
    print(f"Transpiling {language.upper()} code: {source_path.name}")
    
    # Step 1: Parse
    print("  [1/5] Parsing...")
    if is_cython:
        ast_node = parse_cython_file(source_path)
        print(f"       Parsed successfully via built-in Cython compiler")
    else:
        ast_node = parse_python_file(source_path)
        print(f"       Parsed successfully")
    
    # Step 2: Normalize
    print("  [2/5] Normalizing AST...")
    if is_cython:
        ast_node = ast_node
    else:
        ast_node = normalize_python_ast(ast_node)

    function_count = sum(
        1 for child in ast_node.children
        if getattr(child, "node_type", None) == "function"
    )

    class_count = sum(
        1 for child in ast_node.children
        if getattr(child, "node_type", None) == "class"
    )

    print(f"       {function_count} functions, {class_count} classes")
    
    # Step 3: Type Inference
    print("  [3/5] Type inference...")
    type_engine = TypeInferenceEngine()
    print("       Type map ready")
    
    # Step 4: Build IR
    print("  [4/5] Building intermediate representation...")
    ir_module = build_ir_from_ast(ast_node)
    for op in ir_module.operations:
        print(op.opcode, op.attributes)
    print(f"       Generated {len(ir_module.operations)} IR operations")
    
    # Step 5: Code Generation
    print("  [5/5] Generating C++ code...")
    config = CppConfig(namespace=namespace)
    cpp_code = generate_cpp_from_ir(ir_module, source_path.stem, config)
    print("       C++ code generated")
    
    # Write output
    if output_path:
        output_path.write_text(cpp_code)
        print(f"\n✓ Generated C++ written to: {output_path}")
    
    return cpp_code


def transpile_project(project_dir: Path, output_dir: Path, namespace: str = "sklearn"):
    """
    Transpile all Python/Cython files in a project.
    
    Args:
        project_dir: Project root directory
        output_dir: Output directory for C++ files
        namespace: C++ namespace
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all Python and Cython files
    python_files = list(project_dir.glob("**/*.py"))
    cython_files = list(project_dir.glob("**/*.pyx"))
    
    print(f"\nTranspiling project: {project_dir}")
    print(f"  Python files: {len(python_files)}")
    print(f"  Cython files: {len(cython_files)}")
    print()
    
    results = {
        'success': [],
        'failed': [],
    }
    
    # Transpile each file
    for source_file in python_files + cython_files:
        try:
            # Determine output path
            rel_path = source_file.relative_to(project_dir)
            output_file = output_dir / rel_path.with_suffix('.cpp')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Transpile
            cpp_code = transpile_python_to_cpp(source_file, output_file, namespace)
            results['success'].append(str(rel_path))
            
        except Exception as e:
            print(f"✗ Failed to transpile {source_file}: {e}")
            results['failed'].append((str(rel_path), str(e)))
    
    # Summary
    print(f"\n{'='*70}")
    print(f"  Transpilation Summary")
    print(f"{'='*70}")
    print(f"Successful: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    
    if results['failed']:
        print("\nFailed files:")
        for path, error in results['failed']:
            print(f"  • {path}: {error}")
    
    return results


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="sklearn transpiler - Convert Python/Cython to C++"
    )
    
    parser.add_argument(
        "input",
        type=Path,
        help="Input file or directory"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file or directory"
    )
    
    parser.add_argument(
        "-n", "--namespace",
        default="sklearn",
        help="C++ namespace (default: sklearn)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.input.is_file():
            # Single file
            output_path = args.output or args.input.with_suffix('.cpp')
            cpp_code = transpile_python_to_cpp(args.input, output_path, args.namespace)
            print(f"\n✓ Transpilation complete!")
            
        elif args.input.is_dir():
            # Directory
            output_dir = args.output or args.input.parent / f"{args.input.name}_cpp"
            transpile_project(args.input, output_dir, args.namespace)
        
        else:
            print(f"Error: {args.input} not found")
            return 1
        
        return 0
    
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
