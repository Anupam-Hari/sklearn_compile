"""
Cython's Node.__init__ is generic: `def __init__(self, pos, **kw)`. This
means scalar fields (e.g. CEnumDefItemNode.name, the actual symbol name
text) are NOT declared anywhere on the class — they only exist as keyword
arguments at the call sites where the parser constructs each node.

This script statically parses Cython's own Parsing.py (and
ParseTreeTransforms.py, where some nodes are synthesized during semantic
analysis rather than raw parsing) using Python's `ast` module, and
extracts, for every `Nodes.X(...)` / `ExprNodes.X(...)` /
`MatchCaseNodes.X(...)` / bare `ModuleNode(...)` call, the UNION of
keyword argument names used across ALL construction sites for that class.

This is still fully deterministic and grammar-complete: it reads the
compiler's own source, not sample .pyx/.pxd files, so every construction
site the parser can ever hit is included — not just the ones sklearn's
Cython sources happen to trigger.

Output: cython_construction_sites.json
"""

import ast
import json
from pathlib import Path
from collections import defaultdict

CYTHON_SRC = Path("cython_src/cython-3.2.9/Cython/Compiler")

# Files where node classes get instantiated. Parsing.py is the primary
# source (raw parse). ParseTreeTransforms.py is included too since some
# projects' parser.py may run default transforms as part of "parsing" —
# flagged separately in the output so you can decide whether those stages
# are in scope for this project's normalize_symbols.py.
SOURCE_FILES = {
    "Parsing.py": "raw_parse",
    "ParseTreeTransforms.py": "semantic_transform",
}

# module aliases -> how a call's func expression identifies a node class
MODULE_ALIASES = {"Nodes", "ExprNodes", "MatchCaseNodes"}
BARE_NAMES_OF_INTEREST = {"ModuleNode"}  # imported directly, not module-qualified


def resolve_class_name(func_node):
    """
    Given the `func` of an ast.Call, return the node class name if this
    call looks like a node constructor (Nodes.Foo(...), ExprNodes.Foo(...),
    MatchCaseNodes.Foo(...), or bare ModuleNode(...)). Otherwise None.
    """
    if isinstance(func_node, ast.Attribute):
        if isinstance(func_node.value, ast.Name) and func_node.value.id in MODULE_ALIASES:
            return func_node.attr
        return None
    if isinstance(func_node, ast.Name):
        if func_node.id in BARE_NAMES_OF_INTEREST:
            return func_node.id
        return None
    return None


def extract_from_file(path, stage_tag, results):
    tree = ast.parse(path.read_text(), filename=str(path))

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        class_name = resolve_class_name(node.func)
        if class_name is None:
            continue

        entry = results[class_name]
        entry["stages"].add(stage_tag)
        entry["call_site_count"] += 1

        # keyword args -> these are the scalar/child field names
        for kw in node.keywords:
            if kw.arg is not None:  # skip **kwargs spreads (arg is None)
                entry["keyword_args"].add(kw.arg)
            else:
                entry["has_kwargs_spread"] = True

        # positional args beyond `pos` (index 0) are rare but possible
        if len(node.args) > 1:
            entry["extra_positional_arg_count"].add(len(node.args) - 1)


def build():
    results = defaultdict(lambda: {
        "stages": set(),
        "call_site_count": 0,
        "keyword_args": set(),
        "has_kwargs_spread": False,
        "extra_positional_arg_count": set(),
    })

    for filename, stage_tag in SOURCE_FILES.items():
        path = CYTHON_SRC / filename
        if not path.exists():
            print(f"WARNING: {path} not found, skipping")
            continue
        extract_from_file(path, stage_tag, results)

    # make JSON-serializable
    output = {}
    for class_name, entry in sorted(results.items()):
        output[class_name] = {
            "node_type": class_name,
            "stages": sorted(entry["stages"]),
            "call_site_count": entry["call_site_count"],
            "keyword_args": sorted(entry["keyword_args"]),
            "has_kwargs_spread": entry["has_kwargs_spread"],
            "extra_positional_arg_count": sorted(entry["extra_positional_arg_count"]),
        }

    return output


if __name__ == "__main__":
    output = build()
    with open("cython_construction_sites.json", "w") as f:
        json.dump(output, f, indent=2, sort_keys=True)
    print(f"Wrote construction-site data for {len(output)} node classes "
          f"to cython_construction_sites.json")
