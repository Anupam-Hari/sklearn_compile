"""
Merges the three grammar-derived sources into one unified manifest:

  1. python_ast_schema.json          -> ast module _fields (Python)
  2. cython_ast_schema.json          -> child_attrs / subexprs (Cython children)
  3. cython_construction_sites.json  -> real keyword args at construction
                                         (Cython scalars + children combined)

For Cython nodes, the union of (2) and (3) is the important step:
  - child_attrs        = nested Node objects to recurse into
  - keyword_args        = every field the parser actually populates
  - keyword_args - child_attrs = SCALAR fields (name text, flags, etc.)
    that a traversal must read directly, not recurse into

Output: unified_ast_schema.json
"""

import json


def build():
    py_schema = json.load(open("python_ast_schema.json"))
    cy_schema = json.load(open("cython_ast_schema.json"))["nodes"]
    cy_construct = json.load(open("cython_construction_sites.json"))

    unified = {"python": {}, "cython": {}}

    # --- Python: _fields already gives scalars + children together,
    # ast module doesn't distinguish child-node fields from scalar fields
    # at the schema level the way Cython does, so we pass through as-is
    # and flag which fields are node-typed vs scalar using a runtime check.
    import ast as ast_mod
    for name, entry in py_schema.items():
        cls = getattr(ast_mod, name, None)
        scalar_fields = []
        child_fields = []
        if cls is not None:
            # Heuristic grounded in ast's own type system: a field is
            # "child" if it's typed as an AST node or list thereof in the
            # grammar; ast doesn't expose this pre-3.13 without a real
            # instance, so we mark unknown rather than guess for <3.13.
            field_types = getattr(cls, "_field_types", None)
            if field_types:
                for f in entry["fields"]:
                    t = str(field_types.get(f, ""))
                    if "AST" in t or "list" in t.lower():
                        child_fields.append(f)
                    else:
                        scalar_fields.append(f)
        unified["python"][name] = {
            **entry,
            "scalar_fields_known": scalar_fields,
            "child_fields_known": child_fields,
            "field_classification_reliable": bool(scalar_fields or child_fields),
        }

    # --- Cython: merge child_attrs (source of truth for recursion) with
    # construction-site keyword_args (source of truth for full field set)
    all_cy_names = set(cy_schema) | set(cy_construct)
    for name in sorted(all_cy_names):
        class_info = cy_schema.get(name, {})
        construct_info = cy_construct.get(name, {})

        child_attrs = set(class_info.get("child_attrs", []))
        keyword_args = set(construct_info.get("keyword_args", []))

        scalar_fields = sorted(keyword_args - child_attrs)
        # fields declared as children by the class but never observed at
        # any construction site we scanned -> worth a human/audit look
        children_never_constructed = sorted(child_attrs - keyword_args)

        unified["cython"][name] = {
            "node_type": name,
            "base_classes": class_info.get("base_classes", []),
            "source_module": class_info.get("source_module"),
            "child_attrs": sorted(child_attrs),
            "scalar_fields": scalar_fields,
            "all_construction_keyword_args": sorted(keyword_args),
            "children_declared_but_never_constructed_in_scanned_files": children_never_constructed,
            "construction_stages": construct_info.get("stages", []),
            "construction_call_site_count": construct_info.get("call_site_count", 0),
            "has_kwargs_spread_at_construction": construct_info.get("has_kwargs_spread", False),
            "found_in_class_hierarchy": name in cy_schema,
            "found_at_construction_site": name in cy_construct,
        }

    return unified


if __name__ == "__main__":
    unified = build()
    with open("unified_ast_schema.json", "w") as f:
        json.dump(unified, f, indent=2, sort_keys=True)

    n_py = len(unified["python"])
    n_cy = len(unified["cython"])
    print(f"Unified schema: {n_py} Python node types, {n_cy} Cython node types")

    # flag interesting mismatches worth a human look
    only_in_hierarchy = [n for n, e in unified["cython"].items()
                          if e["found_in_class_hierarchy"] and not e["found_at_construction_site"]]
    only_at_construction = [n for n, e in unified["cython"].items()
                             if e["found_at_construction_site"] and not e["found_in_class_hierarchy"]]
    print(f"\nCython classes with NO construction site found in Parsing.py/"
          f"ParseTreeTransforms.py ({len(only_in_hierarchy)}):")
    print("  (these may be: abstract base classes, nodes only synthesized "
          "elsewhere, e.g. optimizer/other transform passes, or dead code)")
    for n in only_in_hierarchy[:20]:
        print(f"    {n}")
    if len(only_in_hierarchy) > 20:
        print(f"    ... and {len(only_in_hierarchy) - 20} more")
