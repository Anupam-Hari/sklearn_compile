"""Modern transpiler package.

Only the current architecture is exposed here. Legacy compatibility modules and
old APIs are intentionally excluded to keep the public surface clear and stable.
"""

__version__ = "0.1.0"
__author__ = "sklearn transpiler contributors"


def __getattr__(name):
    """Lazily resolve the supported public API."""
    if name == "transpile_python_to_cpp":
        from transpiler.pipeline_new import transpile_python_to_cpp
        return transpile_python_to_cpp
    if name == "verify_pipeline":
        from transpiler.main import verify_pipeline
        return verify_pipeline
    if name == "analyze_project":
        from transpiler.project.analyze import analyze_project
        return analyze_project
    if name == "find_symbol":
        from transpiler.dependency.resolver import find_symbol
        return find_symbol
    if name == "parse_python_file":
        from transpiler.parser.python_parser import parse_python_file
        return parse_python_file
    if name == "parse_cython_robust":
        from transpiler.parser.cython_robust_parser import parse_cython_robust
        return parse_cython_robust
    if name == "normalize_python_ast":
        from transpiler.normalizer.python_normalizer import normalize_python_ast
        return normalize_python_ast
    if name == "build_ir":
        from transpiler.ir.builder_new import build_ir_from_ast as build_ir
        return build_ir
    if name == "build_ir_from_ast":
        from transpiler.ir.builder_new import build_ir_from_ast
        return build_ir_from_ast
    if name == "convert_python_ast_to_ir":
        from transpiler.ir.python_to_ir import convert_python_ast_to_ir
        return convert_python_ast_to_ir
    if name == "generate_cpp_from_ir":
        from transpiler.codegen.cpp_generator_new import generate_cpp_from_ir
        return generate_cpp_from_ir
    if name == "cli_main":
        from transpiler.cli.cli import main as cli_main
        return cli_main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "transpile_python_to_cpp",
    "verify_pipeline",
    "analyze_project",
    "find_symbol",
    "parse_python_file",
    "parse_cython_robust",
    "normalize_python_ast",
    "build_ir",
    "build_ir_from_ast",
    "convert_python_ast_to_ir",
    "generate_cpp_from_ir",
    "cli_main",
]
