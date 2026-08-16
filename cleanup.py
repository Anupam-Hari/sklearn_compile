"""
Cleanup script - Remove redundant and unused files.

This identifies files that should be deleted to clean up the codebase.
"""

import os
import sys
from pathlib import Path


def identify_redundant_files():
    """Identify files to be deleted."""
    base = Path("/home/anupam/projects/sklearn_compile")
    
    # Files/dirs to delete (redundant/unused)
    to_delete = [
        # Old Cython parsing (replaced by robust parser)
        "transpiler/cython/block_parser.py",
        "transpiler/cython/improved_parser.py",
        "transpiler/cython/ir.py",
        "transpiler/cython/statement_parser.py",
        
        # Unused CLI tools (just wrappers)
        "transpiler/cli/discover.py",
        "transpiler/cli/extract_imports.py",
        "transpiler/cli/extract_symbols.py",
        "transpiler/cli/inspect_ast.py",
        "transpiler/cli/normalize_python.py",
        "transpiler/cli/parse_python.py",
        
        # Unused cython-specific tools
        "transpiler/cython/calls.py",
        "transpiler/cython/classifier.py",
        "transpiler/cython/dependency_graph.py",
        "transpiler/cython/finder.py",
        "transpiler/cython/method_resolver.py",
        "transpiler/cython/operation_map.py",  # sklearn-specific
        "transpiler/cython/variable_types.py",
        "transpiler/cython/visitor.py",
        
        # Unused dependency tools (sklearn-specific analysis)
        "transpiler/dependency/builtin_types.py",
        "transpiler/dependency/calls.py",
        "transpiler/dependency/class_members.py",
        "transpiler/dependency/class_type_map.py",
        "transpiler/dependency/constructor_parameters.py",
        "transpiler/dependency/cython_methods.py",
        "transpiler/dependency/discover.py",
        "transpiler/dependency/filter.py",
        "transpiler/dependency/instantiations.py",
        "transpiler/dependency/local_symbols.py",
        "transpiler/dependency/member_assignments.py",
        "transpiler/dependency/method_calls.py",
        "transpiler/dependency/type_normalizer.py",
        "transpiler/dependency/walker.py",
        
        # Unused symbol tools
        "transpiler/symbols/",
        
        # Unused graph tools
        "transpiler/graph/",
        
        # Old pipeline examples
        "transpiler/pipeline/",
        
        # Old normalizer for Cython
        "transpiler/normalizer/cython_normalizer.py",
        
        # Old parser files
        "transpiler/parser/splitter_parser.py",
        "transpiler/parser/models.py",
        
        # Old documentation
        "transpiler/README.md",
        
        # Old IR builder (sklearn-specific)
        "transpiler/ir/builder.py",
        "transpiler/ir/control.py",
        "transpiler/cython/ir_builder.py",
        "transpiler/cython/method_extractor.py",
    ]
    
    print("=" * 70)
    print("  REDUNDANT FILES TO DELETE")
    print("=" * 70)
    print()
    
    total_size = 0
    for path_str in to_delete:
        full_path = base / path_str
        
        if full_path.is_dir():
            size = sum(f.stat().st_size for f in full_path.rglob('*') if f.is_file())
            print(f"DIR:  {path_str:50} (~{size:,} bytes)")
        elif full_path.is_file():
            size = full_path.stat().st_size
            print(f"FILE: {path_str:50} ({size:,} bytes)")
        else:
            print(f"N/A:  {path_str:50} (not found)")
            continue
        
        total_size += size
    
    print()
    print(f"Total to delete: ~{total_size:,} bytes")
    print()
    
    return to_delete, base


def delete_files(to_delete, base):
    """Delete identified redundant files."""
    import shutil
    
    print("Deleting files...")
    for path_str in to_delete:
        full_path = base / path_str
        
        if not full_path.exists():
            continue
        
        try:
            if full_path.is_dir():
                shutil.rmtree(full_path)
                print(f"✓ Deleted directory: {path_str}")
            else:
                full_path.unlink()
                print(f"✓ Deleted file: {path_str}")
        except Exception as e:
            print(f"✗ Failed to delete {path_str}: {e}")
    
    print()
    print("Cleanup complete!")


if __name__ == "__main__":
    to_delete, base = identify_redundant_files()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        confirm = input("Delete these files? (y/N): ")
        if confirm.lower() == 'y':
            delete_files(to_delete, base)
    else:
        print("Run with --execute flag to actually delete files:")
        print("  python3 cleanup.py --execute")
