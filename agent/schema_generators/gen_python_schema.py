"""
Generates a COMPLETE, grammar-derived schema of every Python `ast` node type.

Source of truth: the `ast` module's own `_fields` / class hierarchy, NOT
sample files. This means every node type the Python grammar can ever
produce is included, regardless of whether any given codebase (e.g.
sklearn) happens to exercise it.

Output: python_ast_schema.json
"""

import ast
import inspect
import json


def get_base_chain(cls):
    """Return the MRO of ast base classes (excluding object/AST) as strings."""
    chain = []
    for base in cls.__mro__[1:]:
        if base is object:
            continue
        chain.append(base.__name__)
    return chain


def classify_category(cls):
    """
    Rough top-level grammar category, based on ast's own abstract base
    classes (mod, stmt, expr, etc.) — this is structural, not guessed.
    """
    for cat in ("mod", "stmt", "expr", "expr_context", "boolop", "operator",
                "unaryop", "cmpop", "comprehension", "excepthandler",
                "arguments", "arg", "keyword", "alias", "withitem",
                "match_case", "pattern", "type_ignore", "type_param"):
        cat_cls = getattr(ast, cat, None)
        if cat_cls is not None and issubclass(cls, cat_cls):
            return cat
    return "other"


def field_type_hint(node_cls, field_name):
    """
    ast doesn't universally expose per-field types pre-3.13, so we don't
    fabricate types we can't verify. We DO check _field_types when present
    (Python 3.13+) and otherwise leave it null rather than guess.
    """
    field_types = getattr(node_cls, "_field_types", None)
    if field_types and field_name in field_types:
        return str(field_types[field_name])
    return None


def build_schema():
    node_classes = [
        obj for name, obj in vars(ast).items()
        if inspect.isclass(obj) and issubclass(obj, ast.AST)
    ]

    schema = {}
    for cls in sorted(node_classes, key=lambda c: c.__name__):
        name = cls.__name__
        if name == "AST":
            continue

        fields = list(getattr(cls, "_fields", ()))
        # attributes like lineno/col_offset — positional metadata, not
        # grammar fields, but useful to record so nothing is assumed.
        attributes = list(getattr(cls, "_attributes", ()))

        schema[name] = {
            "language": "python",
            "node_type": name,
            "category": classify_category(cls),
            "base_classes": get_base_chain(cls),
            "fields": fields,
            "field_types": {f: field_type_hint(cls, f) for f in fields},
            "positional_attributes": attributes,
            "is_leaf": len(fields) == 0,
        }

    return schema


if __name__ == "__main__":
    schema = build_schema()
    with open("python_ast_schema.json", "w") as f:
        json.dump(schema, f, indent=2, sort_keys=True)
    print(f"Wrote {len(schema)} Python AST node types to python_ast_schema.json")
