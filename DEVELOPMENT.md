"""
Development Guide for sklearn Transpiler Contributors

This guide helps developers understand the codebase and make contributions.
"""

# Architecture Overview

The transpiler follows a classic compiler architecture:

```
┌─────────────────────────┐
│  Source Files           │  .py, .pyx files
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Frontend               │  Project Discovery & Parsing
├─────────────────────────┤
│ • Project Analysis      │  (transpiler/project/)
│ • Source Parsing        │  (transpiler/parser/)
│ • AST Normalization     │  (transpiler/normalizer/)
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Middle-End             │  Intermediate Representation
├─────────────────────────┤
│ • IR Building           │  (transpiler/ir/)
│ • Dependency Analysis   │  (transpiler/dependency/)
│ • Symbol Resolution     │  (transpiler/symbols/)
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Back-End (TODO)        │  Code Generation
├─────────────────────────┤
│ • Type Inference        │  (transpiler/type_inference/)
│ • Code Generation       │  (transpiler/codegen/)
│ • Optimization          │  (transpiler/optimizer/)
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  Output                 │  C/C++/LLVM code
└─────────────────────────┘
```


# Key Design Patterns Used

1. **Visitor Pattern**: Walking AST trees
   - GraphWalker, RecursiveWalker in transpiler/graph/

2. **Builder Pattern**: Creating complex structures
   - IRGraphBuilder, ProjectIndexBuilder

3. **Pipeline Pattern**: Sequential processing
   - Project analysis → Parsing → Normalization → IR

4. **Strategy Pattern**: Different parsing for Python vs Cython
   - PythonParser vs CythonParser

5. **Factory Pattern**: Creating appropriate node types
   - NodeFactory for AST nodes


# Adding a New Feature

## Adding Support for a New AST Node Type

1. **Define the Node** (transpiler/ast/nodes.py):
```python
from dataclasses import dataclass

@dataclass
class NewNode:
    name: str
    attributes: dict = field(default_factory=dict)
```

2. **Add Parsing** (transpiler/parser/python_parser.py):
```python
def parse_new_construct(self, node):
    return NewNode(
        name=node.name,
        attributes=extract_attributes(node)
    )
```

3. **Add Normalization** (transpiler/normalizer/python_normalizer.py):
```python
elif isinstance(node, ast.NewConstruct):
    return NewNode(
        name=node.name,
        attributes={...}
    )
```

4. **Add IR Building** (transpiler/ir/python_to_ir.py):
```python
elif isinstance(node, NewNode):
    self.graph.add(IROperation(
        opcode="NewOperation",
        inputs=[...],
        outputs=[...]
    ))
```

5. **Add Tests** (test your new feature):
```python
def test_new_node_parsing():
    code = "..."
    ast = parse_python_file(code)
    assert isinstance(ast.children[0], NewNode)
```


## Adding a New IR Operation

1. **Define the Operation** (transpiler/ir/models.py):
```python
@dataclass
class NewIROperation(IROperation):
    specific_attribute: str = ""
```

2. **Add Builder Function** (transpiler/ir/builder.py):
```python
def new_operation(input_val, output_val) -> IROperation:
    return IROperation(
        opcode="NewOp",
        inputs=[input_val],
        outputs=[output_val]
    )
```

3. **Add to Operation Map** (transpiler/cython/operation_map.py):
```python
OPERATION_MAP = {
    "new_function": "NewOp",
    ...
}
```

4. **Use in IR Builder** (transpiler/ir/python_to_ir.py):
```python
self.graph.add(
    new_operation(input_val, output_val)
)
```


## Adding a CLI Command

1. **Create Command Handler** (transpiler/cli/cli.py):
```python
def cmd_new_command(args):
    """Handle new-command."""
    print(f"Running new command with args: {args}")
    # Implementation
    return 0
```

2. **Register Subcommand** (transpiler/cli/cli.py):
```python
new_parser = subparsers.add_parser(
    "new-command",
    help="Description of new command"
)
new_parser.add_argument(
    "input",
    type=Path,
    help="Input file"
)
new_parser.set_defaults(func=cmd_new_command)
```

3. **Test Command**:
```bash
python3 -m transpiler new-command --help
python3 -m transpiler new-command input.py
```


# Testing Guide

## Running All Tests
```bash
python3 test_transpiler.py
```

## Testing Individual Components
```bash
# Test Python parsing
python3 -c "from transpiler import parse_python_file; parse_python_file('examples/sample.py')"

# Test normalization
python3 -c "
from transpiler import parse_python_file, normalize_python_ast
ast = parse_python_file('examples/sample.py')
norm = normalize_python_ast(ast)
print(f'Functions: {len(norm.functions)}')
"

# Test IR building
python3 -c "
from transpiler import parse_python_file, normalize_python_ast, convert_python_ast_to_ir
ast = parse_python_file('examples/sample.py')
norm = normalize_python_ast(ast)
ir = convert_python_ast_to_ir(norm)
print(f'Operations: {len(ir.operations)}')
"

# Test project analysis
python3 -m transpiler analyze sklearn/sklearn/tree
```

## Writing Tests

1. **Test Structure**:
```python
def test_feature_name():
    \"\"\"Test description.\"\"\"
    # Arrange: Set up test data
    input_data = ...
    
    # Act: Execute the feature
    result = feature_function(input_data)
    
    # Assert: Verify results
    assert result is not None
    assert result.expected_property == expected_value
```

2. **Add to test_transpiler.py**:
```python
def test_my_new_feature():
    \"\"\"Test my new feature.\"\"\"
    try:
        # Test implementation
        result = my_new_feature()
        assert result is not None
        print("  ✓ My new feature works")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

# Add to tests list in main()
tests = [
    test_my_new_feature,
    ...
]
```


# Code Style Guide

1. **Use Type Hints**:
```python
def process_file(path: Path) -> Optional[AST]:
    ...
```

2. **Use Dataclasses**:
```python
from dataclasses import dataclass, field

@dataclass
class MyData:
    name: str
    items: list = field(default_factory=list)
```

3. **Document Functions**:
```python
def my_function(arg1: str, arg2: int) -> bool:
    \"\"\"
    Short description.
    
    Longer description with details.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    
    Returns:
        Description of return value
    \"\"\"
    ...
```

4. **Use Descriptive Names**:
- Variables: lowercase_with_underscores
- Functions: lowercase_with_underscores
- Classes: CamelCase
- Constants: UPPERCASE_WITH_UNDERSCORES

5. **Keep Functions Small** (< 50 lines ideally)

6. **Error Handling**:
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return None
```


# Debugging Tips

1. **Print Debugging**:
```python
print(f"DEBUG: variable = {variable}")
print(f"DEBUG: type = {type(variable)}")
print(f"DEBUG: dir = {dir(variable)}")
```

2. **Use the Verbose Flag**:
```bash
python3 -m transpiler --verbose <command>
```

3. **Inspect AST**:
```bash
python3 -m transpiler parse file.py --format tree
```

4. **Python Debugger**:
```python
import pdb; pdb.set_trace()  # Set breakpoint
# or
breakpoint()  # Python 3.7+
```


# Performance Optimization

1. **Profile Code**:
```python
import cProfile
cProfile.run('function_to_profile()')
```

2. **Identify Bottlenecks**:
- Project analysis: Use caching for repeated lookups
- Parsing: Cache parsed ASTs
- Normalization: Consider lazy evaluation

3. **Caching Strategies**:
- Memoize expensive functions
- Cache file contents between operations
- Build dependency graph only once


# Release Process

1. **Update Version** (transpiler/__init__.py):
```python
__version__ = "0.2.0"
```

2. **Update Documentation**

3. **Run Full Test Suite**:
```bash
python3 test_transpiler.py
python3 -m transpiler verify
```

4. **Create Release Notes**

5. **Tag Release**:
```bash
git tag v0.2.0
```


# Resources

- Python AST docs: https://docs.python.org/3/library/ast.html
- Cython docs: https://cython.readthedocs.io/
- sklearn docs: https://scikit-learn.org/

# Questions?

Check existing code for patterns, review docstrings, and test changes
thoroughly before submitting.
"""

if __name__ == "__main__":
    print(__doc__)
