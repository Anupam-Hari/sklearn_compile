"""Command-line interface for the sklearn transpiler.

This module provides subcommands for various transpilation tasks:
- analyze: Analyze sklearn project structure
- parse: Parse Python/Cython files
- build-ir: Build intermediate representation
- codegen: Generate C/C++ code (future)
- verify: Verify the full pipeline
"""

import sys
from pathlib import Path
from argparse import ArgumentParser


def create_parser() -> ArgumentParser:
    """Create the root argument parser."""
    parser = ArgumentParser(
        prog="transpiler",
        description="sklearn transpiler - Convert Python to C/C++",
        epilog="For help on a subcommand, use: transpiler <command> --help"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze sklearn project structure"
    )
    analyze_parser.add_argument(
        "project_path",
        type=Path,
        nargs="?",
        default=Path(__file__).parent.parent.parent / "sklearn" / "sklearn" / "tree",
        help="Path to sklearn project (default: sklearn/sklearn/tree)"
    )
    analyze_parser.set_defaults(func=cmd_analyze)

    # Parse command
    parse_parser = subparsers.add_parser(
        "parse",
        help="Parse Python/Cython files"
    )
    parse_parser.add_argument(
        "file_path",
        type=Path,
        help="File to parse"
    )
    parse_parser.add_argument(
        "--format",
        choices=["json", "tree", "text"],
        default="tree",
        help="Output format (default: tree)"
    )
    parse_parser.set_defaults(func=cmd_parse)

    # Build IR command
    ir_parser = subparsers.add_parser(
        "build-ir",
        help="Build intermediate representation"
    )
    ir_parser.add_argument(
        "file_path",
        type=Path,
        help="File to convert to IR"
    )
    ir_parser.add_argument(
        "--output",
        type=Path,
        help="Output file for IR"
    )
    ir_parser.set_defaults(func=cmd_build_ir)

    # Verify command
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify the full transpilation pipeline"
    )
    verify_parser.set_defaults(func=cmd_verify)

    return parser


def cmd_analyze(args):
    """Handle analyze command."""
    from transpiler.project.analyze import analyze_project

    print(f"Analyzing project: {args.project_path}")

    try:
        graph = analyze_project(args.project_path)
        print(f"✓ Found {len(graph.files)} source files")
        print(f"✓ Extracted {sum(len(s) for s in graph.symbols.values())} symbols")
        print(f"✓ Mapped {sum(len(i) for i in graph.imports.values())} imports")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_parse(args):
    """Handle parse command."""
    from transpiler.parser.python_parser import parse_python_file
    from transpiler.normalizer.python_normalizer import normalize_python_ast

    print(f"Parsing: {args.file_path}")

    try:
        ast_node = parse_python_file(args.file_path)
        normalized = normalize_python_ast(ast_node)

        if args.format == "tree":
            _print_ast_tree(normalized)
        elif args.format == "text":
            print(f"Functions: {len(normalized.functions)}")
            print(f"Classes: {len(normalized.classes)}")
            print(f"Imports: {len(normalized.imports)}")

        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_build_ir(args):
    """Handle build-ir command."""
    from transpiler.parser.python_parser import parse_python_file
    from transpiler.normalizer.python_normalizer import normalize_python_ast
    from transpiler.ir.python_to_ir import convert_python_ast_to_ir

    print(f"Building IR for: {args.file_path}")

    try:
        ast_node = parse_python_file(args.file_path)
        normalized = normalize_python_ast(ast_node)
        ir_graph = convert_python_ast_to_ir(normalized)

        print(f"✓ Built IR with {len(ir_graph.operations)} operations")

        for i, op in enumerate(ir_graph.operations[:10]):
            print(f"  {i+1}. {op.opcode}")

        if len(ir_graph.operations) > 10:
            print(f"  ... and {len(ir_graph.operations) - 10} more")

        if args.output:
            print(f"Output would be saved to: {args.output}")

        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_verify(args):
    """Handle verify command."""
    from transpiler.main import verify_pipeline

    try:
        success = verify_pipeline()
        return 0 if success else 1
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def _print_ast_tree(node, indent=0):
    """Print AST tree structure."""
    from transpiler.ast.nodes import ModuleNode

    if isinstance(node, ModuleNode):
        print("  " * indent + "Module")
        for func in node.functions:
            print("  " * (indent + 1) + f"def {func.name}()")
        for cls in node.classes:
            print("  " * (indent + 1) + f"class {cls.name}:")
            for method in cls.methods:
                print("  " * (indent + 2) + f"def {method.name}()")
        if node.imports:
            print("  " * (indent + 1) + "Imports:")
            for imp in node.imports:
                print("  " * (indent + 2) + f"from {imp.module} import {imp.names}")


def main():
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
