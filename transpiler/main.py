#!/usr/bin/env python3
"""Main entry point for the modern transpiler pipeline."""

import sys
import argparse
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PACKAGE_DIR.parent

# Remove the package directory from sys.path so the stdlib ast module is not
# shadowed by the local transpiler/ast package when this file is executed as a
# script. The project root is what should be importable.
for entry in list(sys.path):
    entry_path = Path(entry).resolve() if entry else None
    if entry_path is not None and entry_path == PACKAGE_DIR:
        sys.path.remove(entry)

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from transpiler.project.analyze import analyze_project
from transpiler.normalizer.python_normalizer import normalize_python_ast
from transpiler.parser.python_parser import parse_python_file
from transpiler.pipeline_new import transpile_python_to_cpp


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
        print("✓ Parsed successfully")

        normalized = normalize_python_ast(ast_node)
        print("✓ Normalized AST")
        print(f"  - Module with {len(normalized.functions)} functions, {len(normalized.classes)} classes")
        return normalized
    except Exception as e:
        print(f"✗ Error parsing file: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_pipeline():
    """Verify the modern transpiler pipeline from source to generated C++."""
    print_section("Modern Transpiler Pipeline Verification")

    project_root = Path(__file__).resolve().parents[1]
    example_path = project_root / "examples" / "sample.py"

    normalized_ast = parse_example_file(example_path)
    if normalized_ast is None:
        print("\n✗ Failed to parse example")
        return False

    try:
        generated_cpp = transpile_python_to_cpp(example_path)
        print("\n✓ Generated C++ code from Python source")
        print(f"  - Preview length: {len(generated_cpp)} chars")
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"\n✗ Failed to generate C++: {exc}")
        import traceback
        traceback.print_exc()
        return False

    print_section("Pipeline Status Summary")
    print("✓ Project analysis: available")
    print("✓ Python parsing: working")
    print("✓ AST normalization: working")
    print("✓ IR generation: working")
    print("✓ C++ generation: working")

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
