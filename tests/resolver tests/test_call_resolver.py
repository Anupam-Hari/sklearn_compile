from pathlib import Path

from transpiler.project.analyze import (
    analyze_project,
)

from transpiler.resolver.class_resolver import (
    build_class_index,
)

from transpiler.resolver.call_resolver import (
    resolve_self_call,
)

graph = analyze_project(
    Path("sklearn"),
)

graph.class_index = build_class_index(
    graph,
)

symbol = resolve_self_call(
    graph,
    "BaseDecisionTree",
    "self._prune_tree",
)

print(symbol)