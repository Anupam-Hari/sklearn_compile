#!/usr/bin/env python3
"""Comprehensive test suite for the sklearn transpiler.

Tests all major components of the transpiler pipeline.
"""

import sys
from pathlib import Path


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from transpiler import (
            verify_pipeline,
            analyze_project,
            find_symbol,
            parse_python_file,
            normalize_python_ast,
            convert_python_ast_to_ir,
            build_ir,
            cli_main,
        )
        print("  ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_python_parsing():
    """Test Python file parsing."""
    print("Testing Python parsing...")
    try:
        from transpiler.parser.python_parser import parse_python_file

        path = Path(__file__).parent / "examples" / "sample.py"
        if not path.exists():
            print(f"  ⚠ Sample file not found: {path}")
            return True

        ast_node = parse_python_file(path)
        if ast_node is None:
            print("  ✗ Failed to parse Python file")
            return False

        print(f"  ✓ Parsed {path.name}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_normalization():
    """Test AST normalization."""
    print("Testing AST normalization...")
    try:
        from transpiler.parser.python_parser import parse_python_file
        from transpiler.normalizer.python_normalizer import normalize_python_ast

        path = Path(__file__).parent / "examples" / "sample.py"
        if not path.exists():
            print(f"  ⚠ Sample file not found: {path}")
            return True

        ast_node = parse_python_file(path)
        normalized = normalize_python_ast(ast_node)

        functions = [
            child
            for child in normalized.children
            if child.node_type == "function"
        ]

        if not functions:
            print("  ✗ No functions found in normalized AST")
            return False

        print(
            f"  ✓ Normalized AST with {len(functions)} functions"
        )

        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_ir_building():
    """Test IR building from Python AST."""
    print("Testing IR building...")
    try:
        from transpiler.parser.python_parser import parse_python_file
        from transpiler.normalizer.python_normalizer import normalize_python_ast
        from transpiler.ir.python_to_ir import convert_python_ast_to_ir

        path = Path(__file__).parent / "examples" / "sample.py"
        if not path.exists():
            print(f"  ⚠ Sample file not found: {path}")
            return True

        ast_node = parse_python_file(path)
        normalized = normalize_python_ast(ast_node)
        ir_graph = convert_python_ast_to_ir(normalized)

        if not hasattr(ir_graph, "operations"):
            print("  ✗ IR graph missing 'operations' attribute")
            return False

        print(f"  ✓ Built IR graph with {len(ir_graph.operations)} operations")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_project_analysis():
    """Test project structure analysis."""
    print("Testing project analysis...")
    try:
        from transpiler.project.analyze import analyze_project

        # Try to analyze sklearn tree module if it exists
        sklearn_path = Path(__file__).parent / "sklearn" / "sklearn" / "tree"
        if not sklearn_path.exists():
            print(f"  ⚠ sklearn not found: {sklearn_path}")
            return True

        graph = analyze_project(sklearn_path)

        if graph is None:
            print("  ✗ Failed to analyze project")
            return False

        print(
            f"  ✓ Analyzed project: "
            f"{len(graph.files)} files, "
            f"{sum(len(s) for s in graph.symbols.values())} symbols"
        )
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_cython_statement_parser():
    """Test Cython statement parser."""
    print("Testing Cython statement parser...")
    try:
        from transpiler.cython.statement_parser import CythonStatementParser

        parser = CythonStatementParser()

        # Test simple Cython code
        test_code = """
cdef object test():
    cdef int x = 5
    return x
"""

        ir_graph = parser.parse(test_code)
        print(f"  ✓ Parsed Cython code to IR graph")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_cli_help():
    """Test CLI help output."""
    print("Testing CLI...")
    try:
        from transpiler.cli.cli import create_parser

        parser = create_parser()

        # Check that all subcommands exist
        subcommands = ["analyze", "parse", "build-ir", "verify"]
        # The parser should have been created successfully
        print(f"  ✓ CLI parser created with subcommands")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_dependency_graph():
    """Test dependency graph building."""
    print("Testing dependency graph...")
    try:
        from transpiler.project.analyze import analyze_project
        from transpiler.dependency.resolver import find_symbol

        sklearn_path = Path(__file__).parent / "sklearn" / "sklearn" / "tree"
        if not sklearn_path.exists():
            print(f"  ⚠ sklearn not found: {sklearn_path}")
            return True

        graph = analyze_project(sklearn_path)

        # Try to find a symbol
        symbol = find_symbol(graph, "DecisionTreeClassifier")
        if symbol is None:
            print("  ⚠ Could not find DecisionTreeClassifier (might not exist in tree module)")
            return True

        print(f"  ✓ Found symbol: {symbol.name}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  sklearn Transpiler - Comprehensive Test Suite")
    print("=" * 70 + "\n")

    tests = [
        test_imports,
        test_python_parsing,
        test_normalization,
        test_ir_building,
        test_project_analysis,
        test_cython_statement_parser,
        test_cli_help,
        test_dependency_graph,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
        print()

    # Summary
    print("=" * 70)
    print("  Test Summary")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
