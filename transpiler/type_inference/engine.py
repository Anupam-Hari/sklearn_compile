"""
Type inference engine for transpiler.

Infers types from code structure and propagates them through the AST.
Handles:
- Variable assignments
- Function parameters and returns
- Type annotations
- Cross-module type resolution
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Any
from enum import Enum


class TypeKind(Enum):
    """Kind of type."""
    PRIMITIVE = "primitive"
    OBJECT = "object"
    ARRAY = "array"
    POINTER = "pointer"
    FUNCTION = "function"
    UNKNOWN = "unknown"


@dataclass
class TypeInfo:
    """Information about a type."""
    name: str
    kind: TypeKind = TypeKind.UNKNOWN
    base_type: Optional['TypeInfo'] = None
    element_type: Optional['TypeInfo'] = None
    attributes: Dict[str, 'TypeInfo'] = field(default_factory=dict)
    methods: Dict[str, 'TypeInfo'] = field(default_factory=dict)
    is_mutable: bool = True
    
    def __repr__(self):
        return f"Type({self.name})"


class TypeInferenceEngine:
    """Infer types in code."""
    
    # Built-in type mappings
    PYTHON_TYPES = {
        'int': TypeInfo('int', TypeKind.PRIMITIVE),
        'float': TypeInfo('float', TypeKind.PRIMITIVE),
        'str': TypeInfo('str', TypeKind.PRIMITIVE),
        'bool': TypeInfo('bool', TypeKind.PRIMITIVE),
        'list': TypeInfo('list', TypeKind.OBJECT),
        'dict': TypeInfo('dict', TypeKind.OBJECT),
        'set': TypeInfo('set', TypeKind.OBJECT),
        'tuple': TypeInfo('tuple', TypeKind.OBJECT),
        'object': TypeInfo('object', TypeKind.OBJECT),
        'None': TypeInfo('None', TypeKind.PRIMITIVE),
    }
    
    CYTHON_TYPES = {
        'int': TypeInfo('int', TypeKind.PRIMITIVE),
        'double': TypeInfo('double', TypeKind.PRIMITIVE),
        'float': TypeInfo('float', TypeKind.PRIMITIVE),
        'long': TypeInfo('long', TypeKind.PRIMITIVE),
        'char': TypeInfo('char', TypeKind.PRIMITIVE),
        'void': TypeInfo('void', TypeKind.PRIMITIVE),
        'bint': TypeInfo('bint', TypeKind.PRIMITIVE),
        'object': TypeInfo('object', TypeKind.OBJECT),
        'cdef': TypeInfo('cdef', TypeKind.OBJECT),
        'cpdef': TypeInfo('cpdef', TypeKind.OBJECT),
    }
    
    def __init__(self):
        self.type_map: Dict[str, TypeInfo] = {}
        self.variable_types: Dict[str, TypeInfo] = {}
        self.function_signatures: Dict[str, Dict[str, TypeInfo]] = {}
        self.class_types: Dict[str, TypeInfo] = {}
        
        # Register built-in types
        self.type_map.update(self.PYTHON_TYPES)
        self.type_map.update(self.CYTHON_TYPES)
    
    def infer_from_value(self, value: Any) -> TypeInfo:
        """Infer type from a Python value."""
        if isinstance(value, int):
            return self.type_map['int']
        elif isinstance(value, float):
            return self.type_map['float']
        elif isinstance(value, str):
            return self.type_map['str']
        elif isinstance(value, bool):
            return self.type_map['bool']
        elif isinstance(value, list):
            return self.type_map['list']
        elif isinstance(value, dict):
            return self.type_map['dict']
        elif value is None:
            return self.type_map['None']
        else:
            return self.type_map['object']
    
    def infer_from_annotation(self, annotation: str, language: str = 'python') -> Optional[TypeInfo]:
        """Infer type from a type annotation."""
        annotation = annotation.strip()
        
        # Check for array types
        if '[' in annotation and ']' in annotation:
            base_type_str = annotation[:annotation.index('[')]
            base_type = self.type_map.get(base_type_str)
            if base_type:
                array_type = TypeInfo(annotation, TypeKind.ARRAY)
                array_type.element_type = base_type
                return array_type
        
        # Check for pointer types
        if annotation.endswith('*'):
            base_type_str = annotation[:-1].strip()
            base_type = self.type_map.get(base_type_str)
            if base_type:
                ptr_type = TypeInfo(annotation, TypeKind.POINTER)
                ptr_type.base_type = base_type
                return ptr_type
        
        # Return registered type or unknown
        return self.type_map.get(annotation, 
                                 TypeInfo(annotation, TypeKind.UNKNOWN))
    
    def register_variable(self, name: str, type_info: TypeInfo):
        """Register a variable's type."""
        self.variable_types[name] = type_info
    
    def get_variable_type(self, name: str) -> Optional[TypeInfo]:
        """Get a variable's inferred type."""
        return self.variable_types.get(name)
    
    def register_class(self, name: str, type_info: TypeInfo):
        """Register a class type."""
        self.class_types[name] = type_info
        self.type_map[name] = type_info
    
    def get_class_type(self, name: str) -> Optional[TypeInfo]:
        """Get a class's type info."""
        return self.class_types.get(name)
    
    def register_function_signature(self, name: str, params: Dict[str, TypeInfo], 
                                   return_type: TypeInfo):
        """Register a function signature."""
        self.function_signatures[name] = {
            'params': params,
            'return': return_type,
        }
    
    def infer_expression_type(self, expr: str) -> Optional[TypeInfo]:
        """Infer type of an expression (simple cases)."""
        expr = expr.strip()
        
        # Variable reference
        if expr.isidentifier():
            return self.variable_types.get(expr)
        
        # Numeric literal
        try:
            int(expr)
            return self.type_map['int']
        except ValueError:
            pass
        
        try:
            float(expr)
            return self.type_map['float']
        except ValueError:
            pass
        
        # String literal
        if expr.startswith('"') and expr.endswith('"'):
            return self.type_map['str']
        if expr.startswith("'") and expr.endswith("'"):
            return self.type_map['str']
        
        # Boolean
        if expr in ('True', 'False'):
            return self.type_map['bool']
        
        # List literal
        if expr.startswith('[') and expr.endswith(']'):
            return self.type_map['list']
        
        # Dict literal
        if expr.startswith('{') and expr.endswith('}'):
            return self.type_map['dict']
        
        # None
        if expr == 'None':
            return self.type_map['None']
        
        # Function call (simple)
        if '(' in expr and ')' in expr:
            func_name = expr[:expr.index('(')]
            if func_name in self.function_signatures:
                return self.function_signatures[func_name].get('return')
        
        # Unknown
        return TypeInfo(expr, TypeKind.UNKNOWN)
    
    def propagate_types(self, ast_node: Any):
        """
        Propagate types through an AST.
        
        Args:
            ast_node: An AST node (generic)
        """
        if not ast_node:
            return
        
        # Simple type propagation for common patterns
        if hasattr(ast_node, 'name') and hasattr(ast_node, 'value'):
            # Variable assignment: x = value
            value_type = self.infer_expression_type(str(ast_node.value))
            if value_type:
                self.register_variable(ast_node.name, value_type)


def create_inference_engine() -> TypeInferenceEngine:
    """Create a type inference engine."""
    return TypeInferenceEngine()


def infer_types_for_code(code: str, language: str = 'python') -> Dict[str, TypeInfo]:
    """
    Infer types for a code snippet.
    
    Args:
        code: Source code
        language: 'python' or 'cython'
    
    Returns:
        Dictionary mapping names to types
    """
    engine = create_inference_engine()
    # Simple parsing - just look for type annotations
    for line in code.split('\n'):
        line = line.strip()
        if ':' in line and '=' in line:
            # Simple type annotation: name: type = value
            parts = line.split(':')
            if len(parts) == 2:
                name = parts[0].strip()
                rest = parts[1].split('=')
                if len(rest) >= 1:
                    type_str = rest[0].strip()
                    type_info = engine.infer_from_annotation(type_str, language)
                    if type_info:
                        engine.register_variable(name, type_info)
    
    return engine.variable_types
