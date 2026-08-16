"""sklearn transpiler - Convert Python to optimized C/C++ code.

Main transpiler package with entry points for analysis, parsing, and code generation.
"""

__version__ = "0.1.0"
__author__ = "sklearn transpiler contributors"

# Core pipeline functions
from transpiler.pipeline_new import transpile_python_to_cpp

# Project analysis
from transpiler.project.analyze import analyze_project
from transpiler.dependency.resolver import find_symbol

# Parsing
from transpiler.parser.python_parser import parse_python_file
from transpiler.parser.cython_robust_parser import parse_cython_robust

# Normalization
from transpiler.normalizer.python_normalizer import normalize_python_ast

# IR generation
from transpiler.ir.builder_new import build_ir_from_ast
from transpiler.ir.python_to_ir import convert_python_ast_to_ir

# Code generation
from transpiler.codegen.cpp_generator_new import generate_cpp_from_ir

# Type inference
from transpiler.type_inference.engine import create_inference_engine

# CLI
from transpiler.cli.cli import main as cli_main

__all__ = [
    # Pipeline
    "verify_pipeline",
    # Analysis
    "analyze_project",
    "find_symbol",
    # Parsing
    "parse_python_file",
    # Normalization
    "normalize_python_ast",
    # IR
    "convert_python_ast_to_ir",
    "build_ir",
    # CLI
    "cli_main",
]
