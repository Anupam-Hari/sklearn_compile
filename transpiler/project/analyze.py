from pathlib import Path

from transpiler.dependency.imports import extract_imports
from transpiler.dependency.symbols import extract_symbols
from transpiler.normalizer.python_normalizer import normalize_python_ast
from transpiler.parser.cython_parser import parse_cython_file
from transpiler.parser.python_parser import parse_python_file
from transpiler.project.index import build_project_index

def analyze_project(root: Path):

    graph = build_project_index(root)

    for path, source_file in graph.files.items():

        try:
            if source_file.language == "python":

                tree = parse_python_file(path)

                module = normalize_python_ast(tree)

                graph.imports[path] = extract_imports(module)

                graph.symbols[path] = extract_symbols(
                    module,
                    path,
                    source_file.language,
                )

            elif source_file.language == "cython":

                module = parse_cython_file(path)
                graph.imports[path] = []
                graph.symbols[path] = [
                    {"name": child.name, "kind": child.node_type}
                    for child in module.children
                ]

        except Exception as e:

            print(f"Skipping {path}: {e}")

            graph.imports[path] = []

            graph.symbols[path] = []

    return graph