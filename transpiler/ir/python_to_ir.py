"""Convert normalized Python AST to IR graph.

This module bridges the gap between Python's ModuleNode AST representation
and the IR graph format used for code generation.
"""

from transpiler.ast.nodes import ModuleNode, FunctionNode, ClassNode
from transpiler.ir.graph import IRGraph
from transpiler.ir.models import IROperation


class PythonToIRConverter:
    """Convert Python AST nodes to IR operations."""

    def __init__(self):
        self.graph = None
        self.function_stack = []

    def convert(self, module_node: ModuleNode) -> IRGraph:
        """
        Convert a Python module to IR graph.

        Args:
            module_node: Normalized Python AST module

        Returns:
            IRGraph representing the module
        """
        self.graph = IRGraph()

        # Convert module-level functions
        for func in module_node.functions:
            self._convert_function(func)

        # Convert classes and their methods
        for cls in module_node.classes:
            self._convert_class(cls)

        return self.graph

    def _convert_function(self, func: FunctionNode):
        """Convert a function definition to IR."""
        # Add function entry point
        self.graph.add(
            IROperation(
                opcode="FunctionEntry",
                inputs=[],
                outputs=[func.name],
                attributes={"name": func.name},
            )
        )

        self.function_stack.append(func.name)

        # Add function exit point (placeholder for now)
        self.graph.add(
            IROperation(
                opcode="FunctionExit",
                inputs=[func.name],
                outputs=[],
                attributes={"name": func.name},
            )
        )

        self.function_stack.pop()

    def _convert_class(self, cls: ClassNode):
        """Convert a class definition to IR."""
        # Add class entry point
        self.graph.add(
            IROperation(
                opcode="ClassEntry",
                inputs=[],
                outputs=[cls.name],
                attributes={"name": cls.name, "bases": cls.bases},
            )
        )

        # Convert class methods
        for method in cls.methods:
            self._convert_function(method)

        # Add class exit point
        self.graph.add(
            IROperation(
                opcode="ClassExit",
                inputs=[cls.name],
                outputs=[],
                attributes={"name": cls.name},
            )
        )


def convert_python_ast_to_ir(module_node: ModuleNode) -> IRGraph:
    """
    Convert a Python ModuleNode to IR graph.

    Args:
        module_node: Normalized Python AST module

    Returns:
        IRGraph representing the Python module
    """
    converter = PythonToIRConverter()
    return converter.convert(module_node)
