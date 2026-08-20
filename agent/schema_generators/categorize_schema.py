"""
Buckets every node type in unified_ast_schema.json into one category:

    declarations   - defines a named symbol (class/func/var/type/enum/struct)
    imports        - import statements
    control_flow   - if/for/while/try/with/match/break/continue/return/raise
    operators      - binop/unop/boolop/compare/augassign operator kinds
    literals       - constant/num/str/bytes/name-atom leaf nodes
    expressions    - other expr-category nodes not covered above
    statements     - other stmt-category nodes not covered above (e.g. Pass)
    other          - doesn't fit cleanly (module root, comprehension helpers, etc.)

Every classification records WHICH rule fired (evidence), so this is
auditable rather than an opaque guess — consistent with "validate before
you trust a categorization" from the project's own methodology.

Input:  unified_ast_schema.json
Output: categorized_ast_schema.json (grouped by category)
        + prints a summary count table
"""

import json
from collections import defaultdict

IMPORT_HINTS = ("Import",)
CONTROL_FLOW_HINTS = (
    "If", "For", "While", "Try", "With", "Match", "Break", "Continue",
    "Return", "Raise", "Except", "Finally", "Case", "Loop", "GotoNode",
    "ContinueStatNode", "BreakStatNode",
)
DECLARATION_SUFFIXES = (
    "DefNode", "FunctionDef", "ClassDef", "VarDefNode", "TypeDefNode",
    "StructOrUnionDefNode", "EnumDefNode", "EnumDefItemNode", "CVarDefNode",
    "Assign", "AnnAssign", "CnameDeclaratorNode", "ArgDecl",
)
DECLARATION_EXACT = {
    "Module", "ModuleNode", "arg", "AnnAssign", "Assign", "AugAssign",
}
OPERATOR_BASE_HINTS = (
    "BinopNode", "UnopNode", "BoolBinopNode", "PrimaryCmpNode",
    "operator", "boolop", "unaryop", "cmpop", "NumBinopNode",
)
OPERATOR_NAME_HINTS = (
    "BinOp", "UnaryOp", "BoolOp", "Compare", "Add", "Sub", "Mult", "Div",
    "Mod", "Pow", "LShift", "RShift", "BitOr", "BitXor", "BitAnd",
    "FloorDiv", "And", "Or", "Not", "Eq", "NotEq", "Lt", "LtE", "Gt",
    "GtE", "Is", "IsNot", "In", "NotIn", "USub", "UAdd", "Invert",
)
LITERAL_HINTS = (
    "Constant", "Num", "Str", "Bytes", "NameConstant", "Ellipsis",
    "IntNode", "FloatNode", "StringNode", "UnicodeNode", "BytesNode",
    "ImagNode", "BoolNode", "NoneNode", "EllipsisNode",
)


def classify_python(name, entry):
    bases = set(entry.get("base_classes", []))
    category = entry.get("category", "")

    if name in DECLARATION_EXACT:
        return "declarations", f"exact match: {name}"
    if "Import" in name:
        return "imports", f"name contains 'Import'"
    if any(h in name for h in CONTROL_FLOW_HINTS):
        return "control_flow", f"name matches control-flow hint"
    if name in ("ClassDef", "FunctionDef", "AsyncFunctionDef", "Lambda", "Global", "Nonlocal"):
        return "declarations", f"exact statement/def match: {name}"
    if category in ("operator", "boolop", "unaryop", "cmpop"):
        return "operators", f"ast category='{category}'"
    if any(h == name for h in OPERATOR_NAME_HINTS):
        return "operators", f"name matches operator hint"
    if category == "expr" and any(h in name for h in LITERAL_HINTS):
        return "literals", f"expr + name matches literal hint"
    if category == "expr":
        return "expressions", f"ast category='expr'"
    if category == "stmt":
        return "statements", f"ast category='stmt' (uncategorized further)"
    return "other", f"ast category='{category or 'unknown'}'"


def classify_cython(name, entry):
    bases = set(entry.get("base_classes", []))

    if name == "ModuleNode":
        return "declarations", "exact match: module root symbol"
    if any(h in name for h in IMPORT_HINTS):
        return "imports", "name contains 'Import'"
    if any(h in name for h in CONTROL_FLOW_HINTS):
        return "control_flow", "name matches control-flow hint"
    if any(name.endswith(suf) for suf in DECLARATION_SUFFIXES):
        return "declarations", f"name ends with declaration suffix"
    if "StatNode" in bases and ("Assign" in name or "Decl" in name):
        return "declarations", "StatNode base + Assign/Decl in name"
    if any(h in bases for h in OPERATOR_BASE_HINTS) or any(h == name or name.startswith(h + "Node") for h in OPERATOR_NAME_HINTS):
        return "operators", "base class or name matches operator hint"
    if any(h == name or name.startswith(h) for h in LITERAL_HINTS):
        return "literals", "name matches literal hint"
    if "ExprNode" in bases or name.endswith("ExprNode") or name.endswith("Node") and "ExprNode" in bases:
        return "expressions", "ExprNode in base chain"
    if "StatNode" in bases:
        return "statements", "StatNode in base chain (uncategorized further)"
    return "other", "no rule matched"


def build():
    unified = json.load(open("unified_ast_schema.json"))

    categorized = {
        "python": defaultdict(dict),
        "cython": defaultdict(dict),
    }
    evidence_log = {"python": {}, "cython": {}}

    for name, entry in unified["python"].items():
        cat, why = classify_python(name, entry)
        categorized["python"][cat][name] = entry
        evidence_log["python"][name] = {"category": cat, "rule": why}

    for name, entry in unified["cython"].items():
        cat, why = classify_cython(name, entry)
        categorized["cython"][cat][name] = entry
        evidence_log["cython"][name] = {"category": cat, "rule": why}

    # convert defaultdicts for json
    categorized = {
        lang: {cat: nodes for cat, nodes in cats.items()}
        for lang, cats in categorized.items()
    }

    return categorized, evidence_log


if __name__ == "__main__":
    categorized, evidence_log = build()

    with open("categorized_ast_schema.json", "w") as f:
        json.dump(categorized, f, indent=2, sort_keys=True)

    with open("categorization_evidence.json", "w") as f:
        json.dump(evidence_log, f, indent=2, sort_keys=True)

    print(f"{'Category':<15} {'Python':>8} {'Cython':>8}")
    print("-" * 33)
    all_cats = sorted(set(categorized["python"]) | set(categorized["cython"]))
    for cat in all_cats:
        py_n = len(categorized["python"].get(cat, {}))
        cy_n = len(categorized["cython"].get(cat, {}))
        print(f"{cat:<15} {py_n:>8} {cy_n:>8}")

    print("\nWrote categorized_ast_schema.json (grouped) "
          "and categorization_evidence.json (per-node rule that fired).")
    print("Review 'other' and 'statements'/'expressions' buckets manually — "
          "those are catch-alls, not confidently classified.")
