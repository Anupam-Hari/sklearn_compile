import unittest
from pathlib import Path

from transpiler.parser.cython_parser import parse_cython_file


class TestCythonParser(unittest.TestCase):
    def test_dump_cython_ast_for_criterion_pyx(self):
        path = Path("sklearn/tree/_criterion.pyx")

        tree = parse_cython_file(path)

        print(tree)

    def test_dump_cython_ast_for_criterion_pxd(self):
        path = Path("sklearn/tree/_criterion.pxd")

        tree = parse_cython_file(path)

        print(tree)


if __name__ == "__main__":
    unittest.main()