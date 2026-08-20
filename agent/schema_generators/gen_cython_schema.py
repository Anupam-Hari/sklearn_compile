"""
Generates a COMPLETE, grammar-derived schema of every Cython compiler node
type (statement nodes from Nodes.py, expression nodes from ExprNodes.py).

Source of truth: `child_attrs` and `__init__`/class body as declared on the
node CLASSES themselves in Cython.Compiler, NOT sample .pyx/.pxd files.
This means every node class the Cython compiler can ever instantiate is
included, regardless of whether sklearn's Cython sources happen to use it.

IMPORTANT: child_attrs (and node class sets) can differ between Cython
versions. Record the installed version so schema drift is traceable if
the project's pinned Cython version differs.

Output: cython_ast_schema.json
"""

import inspect
import json

import Cython
from Cython.Compiler import Nodes, ExprNodes


def get_own_and_inherited_child_attrs(cls):
    """
    child_attrs is declared per-class (often overriding the parent's list
    entirely, per Cython convention) — record both the resolved value
    (what you actually traverse) and whether this class declares its own
    or falls back to an ancestor's.

    Wrinkle: on ExprNode, `child_attrs` is not a plain list — it's a
    property aliased to `subexprs` (operator.attrgetter('subexprs')).
    So for expression nodes the REAL per-class traversal list lives in
    the `subexprs` class attribute, and we must resolve through that
    instead of reading `child_attrs` directly (which would just be a
    property object, not a list).
    """
    raw = cls.__dict__.get("child_attrs", None)
    if isinstance(raw, property):
        # property-based (ExprNode family) -> resolve via subexprs
        resolved = getattr(cls, "subexprs", None)
        declared_directly = "subexprs" in cls.__dict__
        return resolved, declared_directly

    if raw is not None:
        # class declares its own concrete child_attrs list
        return raw, True

    # not declared on this class directly -> walk up MRO for resolution
    resolved = getattr(cls, "child_attrs", None)
    if isinstance(resolved, property):
        resolved = getattr(cls, "subexprs", None)
    return resolved, False


def get_base_chain(cls, stop_at):
    chain = []
    for base in cls.__mro__[1:]:
        chain.append(base.__name__)
        if base is stop_at:
            break
    return chain


def collect_declared_attrs_from_init(cls):
    """
    Best-effort: pull attribute names assigned in the class's OWN __init__
    (self.x = ...) via source inspection. This is supplementary evidence
    only — child_attrs remains the authoritative traversal source. Useful
    for spotting attrs that hold symbol-relevant data but aren't in
    child_attrs (e.g. scalar `name` fields, which usually aren't children
    but ARE where the symbol name text lives).
    """
    init = cls.__dict__.get("__init__")
    if init is None:
        return []
    try:
        src = inspect.getsource(init)
    except (OSError, TypeError):
        return []
    import re
    attrs = sorted(set(re.findall(r"self\.([A-Za-z_][A-Za-z0-9_]*)\s*=", src)))
    return attrs


def build_schema_for_module(module, base_class, language_tag):
    schema = {}
    for name, cls in vars(module).items():
        if not inspect.isclass(cls):
            continue
        if not issubclass(cls, base_class):
            continue
        if cls is base_class:
            continue

        child_attrs, declared_directly = get_own_and_inherited_child_attrs(cls)
        init_attrs = collect_declared_attrs_from_init(cls)

        schema[name] = {
            "language": language_tag,
            "node_type": name,
            "source_module": module.__name__,
            "base_classes": get_base_chain(cls, base_class),
            "child_attrs": list(child_attrs) if child_attrs else [],
            "child_attrs_declared_directly": declared_directly,
            "init_assigned_attrs": init_attrs,
            "is_leaf": not child_attrs,
        }

    return schema


if __name__ == "__main__":
    stat_schema = build_schema_for_module(Nodes, Nodes.Node, "cython")
    expr_schema = build_schema_for_module(ExprNodes, ExprNodes.ExprNode, "cython")

    # ExprNode IS-A Node subtree in Cython, so de-dupe if a class appears
    # reachable from both imports (shouldn't normally happen, but be safe)
    combined = {**stat_schema, **expr_schema}

    output = {
        "_meta": {
            "cython_version": Cython.__version__,
            "total_node_types": len(combined),
            "stat_node_types": len(stat_schema),
            "expr_node_types": len(expr_schema),
        },
        "nodes": combined,
    }

    with open("cython_ast_schema.json", "w") as f:
        json.dump(output, f, indent=2, sort_keys=True)

    print(f"Cython version: {Cython.__version__}")
    print(f"Wrote {len(combined)} Cython node types "
          f"({len(stat_schema)} stat + {len(expr_schema)} expr) "
          f"to cython_ast_schema.json")
