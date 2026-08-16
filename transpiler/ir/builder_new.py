"""
Generalized IR builder - domain-independent intermediate representation.

This replaces the sklearn-specific IR builder and makes it work for any code.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from transpiler.ir.models import IROperation, IRModule


@dataclass
class IRBuilder:
    """Build IR from AST in a domain-agnostic way."""
    
    def __init__(self):
        self.graph = IRModule()
        self.current_scope = {}
        self.scope_stack = []
    
    def build_from_ast(self, ast_node: Any) -> IRModule:
        """Build IR from any AST node."""
        self.graph = IRModule()
        
        # Handle different node types
        if hasattr(ast_node, '__class__'):
            class_name = ast_node.__class__.__name__
            
            if class_name == 'ModuleNode':
                self._build_module(ast_node)
            elif class_name == 'FunctionNode':
                self._build_function(ast_node)
            elif class_name == 'ClassNode':
                self._build_class(ast_node)
            elif class_name == 'BlockNode':  # Cython
                self._build_block(ast_node)
        
        return self.graph
    
    def _build_module(self, node):
        """Build IR from a module node."""
        # Process imports
        for imp in getattr(node, 'imports', []):
            self._add_import_op(imp)
        
        # Process functions
        for func in getattr(node, 'functions', []):
            self._build_function(func)
        
        # Process classes
        for cls in getattr(node, 'classes', []):
            self._build_class(cls)
    
    def _build_function(self, func):
        """Build IR from a function node."""
        func_name = getattr(func, 'name', 'unknown')
        
        # Add function entry
        self.graph.add(IROperation(
            opcode="FunctionEntry",
            inputs=[],
            outputs=[func_name],
            attributes={'name': func_name}
        ))
        
        # Process function body (simplified)
        if hasattr(func, 'body'):
            self._build_block(func.body)
        
        # Add function exit
        self.graph.add(IROperation(
            opcode="FunctionExit",
            inputs=[func_name],
            outputs=[],
            attributes={'name': func_name}
        ))
    
    def _build_class(self, cls):
        """Build IR from a class node."""
        cls_name = getattr(cls, 'name', 'unknown')
        bases = getattr(cls, 'bases', [])
        
        # Add class entry
        self.graph.add(IROperation(
            opcode="ClassEntry",
            inputs=[],
            outputs=[cls_name],
            attributes={'name': cls_name, 'bases': bases}
        ))
        
        # Process methods
        for method in getattr(cls, 'methods', []):
            self._build_function(method)
        
        # Add class exit
        self.graph.add(IROperation(
            opcode="ClassExit",
            inputs=[cls_name],
            outputs=[],
            attributes={'name': cls_name}
        ))
    
    def _build_block(self, block):
        """Build IR from a Cython block node."""
        if not hasattr(block, 'kind'):
            return
        
        kind = block.kind
        
        if kind == 'while':
            self.graph.add(IROperation(
                opcode="BeginLoop",
                inputs=[],
                outputs=[],
                attributes={'type': 'while'}
            ))
        elif kind == 'for':
            self.graph.add(IROperation(
                opcode="BeginLoop",
                inputs=[],
                outputs=[],
                attributes={'type': 'for'}
            ))
        elif kind == 'if':
            condition = getattr(block, 'condition', None)
            self.graph.add(IROperation(
                opcode="Branch",
                inputs=[condition] if condition else [],
                outputs=[],
                attributes={'condition': condition}
            ))
        
        # Process children
        for child in getattr(block, 'children', []):
            self._build_block(child)
        
        # Close blocks
        if kind in ('while', 'for'):
            self.graph.add(IROperation(
                opcode="EndLoop",
                inputs=[],
                outputs=[],
                attributes={'type': kind}
            ))
    
    def _add_import_op(self, imp):
        """Add an import operation to IR."""
        if isinstance(imp, dict):
            module = imp.get('module', 'unknown')
        elif hasattr(imp, 'module'):
            module = imp.module
        else:
            return
        
        self.graph.add(IROperation(
            opcode="Import",
            inputs=[],
            outputs=[module],
            attributes={'module': module}
        ))


def build_ir_from_ast(ast_node: Any) -> IRModule:
    """
    Build IR from any AST node.
    
    Args:
        ast_node: Normalized AST node
    
    Returns:
        IR module
    """
    builder = IRBuilder()
    return builder.build_from_ast(ast_node)
