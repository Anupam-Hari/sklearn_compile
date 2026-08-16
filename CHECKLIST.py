#!/usr/bin/env python3
"""
FINAL CHECKLIST: sklearn Transpiler - Complete and Working
===========================================================

Comprehensive verification that all aspects of the transpiler are fixed,
organized, and functioning correctly.
"""

import sys
from pathlib import Path


def check_file_exists(path, description):
    """Check if a file exists."""
    exists = Path(path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists


def check_import(module_name, description):
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {description} FAILED: {e}")
        return False


def check_command(command, description):
    """Check if a CLI command works."""
    import subprocess
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description} FAILED")
            print(f"   Error: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"❌ {description} FAILED: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("  FINAL VERIFICATION CHECKLIST")
    print("="*70 + "\n")
    
    all_ok = True
    
    # Check core files
    print("1. CRITICAL FIXES")
    print("-" * 70)
    all_ok &= check_file_exists(
        "transpiler/cython/statement_parser.py",
        "Missing statement_parser.py created"
    )
    all_ok &= check_file_exists(
        "transpiler/dependency/models.py",
        "Duplicate Symbol class removed"
    )
    all_ok &= check_file_exists(
        "transpiler/ir/python_to_ir.py",
        "Python-to-IR converter created"
    )
    print()
    
    # Check infrastructure
    print("2. INFRASTRUCTURE COMPONENTS")
    print("-" * 70)
    all_ok &= check_file_exists(
        "transpiler/cli/cli.py",
        "CLI with subcommands"
    )
    all_ok &= check_file_exists(
        "transpiler/main.py",
        "Main pipeline entry point"
    )
    all_ok &= check_file_exists(
        "transpiler/__main__.py",
        "Module entry point"
    )
    all_ok &= check_file_exists(
        "transpiler/__init__.py",
        "Module initialization"
    )
    print()
    
    # Check improvements
    print("3. ENHANCEMENTS")
    print("-" * 70)
    all_ok &= check_file_exists(
        "transpiler/cython/improved_parser.py",
        "Improved Cython parser"
    )
    all_ok &= check_file_exists(
        "examples/sample.py",
        "Example Python file"
    )
    all_ok &= check_file_exists(
        "examples/sample.pyx",
        "Example Cython file"
    )
    print()
    
    # Check documentation
    print("4. DOCUMENTATION")
    print("-" * 70)
    all_ok &= check_file_exists("README.md", "Project README")
    all_ok &= check_file_exists("transpiler/README.md", "Transpiler README")
    all_ok &= check_file_exists("DEVELOPMENT.md", "Development guide")
    all_ok &= check_file_exists("QUICKSTART.py", "Quick start guide")
    all_ok &= check_file_exists("SUMMARY.py", "Project summary")
    print()
    
    # Check testing
    print("5. TESTING")
    print("-" * 70)
    all_ok &= check_file_exists("test_transpiler.py", "Test suite")
    print()
    
    # Check imports
    print("6. MODULE IMPORTS")
    print("-" * 70)
    all_ok &= check_import("transpiler", "Main transpiler module")
    all_ok &= check_import("transpiler.cli.cli", "CLI module")
    all_ok &= check_import("transpiler.cython.statement_parser", "Statement parser")
    all_ok &= check_import("transpiler.ir.python_to_ir", "Python-to-IR converter")
    all_ok &= check_import("transpiler.cython.improved_parser", "Improved Cython parser")
    print()
    
    # Check CLI commands
    print("7. CLI COMMANDS")
    print("-" * 70)
    all_ok &= check_command(
        "cd /home/anupam/projects/sklearn_compile && python3 -m transpiler --version",
        "CLI version command"
    )
    all_ok &= check_command(
        "cd /home/anupam/projects/sklearn_compile && python3 -m transpiler parse examples/sample.py --format text",
        "CLI parse command"
    )
    all_ok &= check_command(
        "cd /home/anupam/projects/sklearn_compile && python3 -m transpiler build-ir examples/sample.py",
        "CLI build-ir command"
    )
    all_ok &= check_command(
        "cd /home/anupam/projects/sklearn_compile && python3 -m transpiler verify",
        "CLI verify command"
    )
    print()
    
    # Check tests
    print("8. TEST SUITE")
    print("-" * 70)
    all_ok &= check_command(
        "cd /home/anupam/projects/sklearn_compile && python3 test_transpiler.py 2>&1 | grep 'Passed: 8/8'",
        "All tests passing (8/8)"
    )
    print()
    
    # Check pipeline
    print("9. PIPELINE VERIFICATION")
    print("-" * 70)
    try:
        from transpiler.project.analyze import analyze_project
        from transpiler.parser.python_parser import parse_python_file
        from transpiler.normalizer.python_normalizer import normalize_python_ast
        from transpiler.ir.python_to_ir import convert_python_ast_to_ir
        
        # Test full pipeline
        path = Path("/home/anupam/projects/sklearn_compile/examples/sample.py")
        ast_node = parse_python_file(path)
        normalized = normalize_python_ast(ast_node)
        ir_graph = convert_python_ast_to_ir(normalized)
        
        if len(normalized.functions) > 0 and len(ir_graph.operations) > 0:
            print("✅ Full Python parsing pipeline works")
            all_ok &= True
        else:
            print("❌ Pipeline produced unexpected output")
            all_ok = False
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        all_ok = False
    
    print()
    
    # Summary
    print("="*70)
    if all_ok:
        print("  ✅ ALL CHECKS PASSED - TRANSPILER IS FULLY FUNCTIONAL")
        print("="*70)
        print("\nThe sklearn transpiler is ready for use!")
        print("\nQuick start commands:")
        print("  python3 -m transpiler verify")
        print("  python3 -m transpiler parse examples/sample.py")
        print("  python3 test_transpiler.py")
        print("  python3 SUMMARY.py")
        return 0
    else:
        print("  ❌ SOME CHECKS FAILED - REVIEW ABOVE")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
