import tempfile
import unittest
from pathlib import Path

from transpiler.ast.nodes import ModuleNode
from transpiler.parser.cython_parser import parse_cython_file


class TestCythonParser(unittest.TestCase):
    def test_parse_cython_uses_native_compiler_and_returns_generic_ast(self):
        source = """cdef class Splitter:\n    cdef int n_features\n\n    cpdef int node_split(self):\n        return 1\n\n\ndef add(a, b):\n    return a + b\n"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.pyx"
            path.write_text(source, encoding="utf-8")
            tree = parse_cython_file(path)

        self.assertIsInstance(tree, ModuleNode)
        self.assertEqual(tree.node_type, "module")
        self.assertGreaterEqual(len(tree.children), 2)
        self.assertEqual(tree.children[0].name, "Splitter")
        self.assertEqual(tree.children[0].methods[0].name, "node_split")
        self.assertEqual(tree.children[1].name, "add")


if __name__ == "__main__":
    unittest.main()