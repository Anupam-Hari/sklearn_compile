from pathlib import Path

from transpiler.dependency.imports import extract_imports
from transpiler.dependency.symbols import extract_symbols
from transpiler.dependency.calls import extract_calls
from transpiler.normalizer.cython_normalizer import (
    normalize_cython_ast,
)
from transpiler.normalizer.python_normalizer import (
    normalize_python_ast,
)
from transpiler.parser.cython_parser import (
    parse_cython_file,
)
from transpiler.parser.python_parser import (
    parse_python_file,
)
from transpiler.project.index import (
    build_project_index,
)


def analyze_project(root: Path):

    graph = build_project_index(root)

    for path, source_file in graph.files.items():

        if "tests" in path.parts:

            continue

        try:

            if source_file.language == "python":

                tree = parse_python_file(path)

                module = normalize_python_ast(tree)

            elif source_file.language == "cython":

                tree = parse_cython_file(path)

                module = normalize_cython_ast(tree)

            else:

                continue

            graph.modules[path] = module

            extract_imports(
                graph,
                module,
                path,
            )

            extract_symbols(
                graph,
                module,
                path,
                source_file.language,
            )

            extract_calls(
                graph,
                module,
                path,
            )

        except Exception as e:

            print(f"Skipping {path}: {e}")

            graph.modules[path] = []

            graph.imports[path] = []

            graph.symbols[path] = []

            graph.calls[path] = []

    return graph