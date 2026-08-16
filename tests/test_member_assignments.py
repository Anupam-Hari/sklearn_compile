from pathlib import Path

from transpiler.project.analyze import analyze_project
from transpiler.dependency.inherited_members import (
    get_all_class_members,
)

graph = analyze_project(
    Path("sklearn")
)

members = get_all_class_members(
    graph,
    "BestSplitter",
)

print(members)

for name, member_type in sorted(
    members.items()
):
    print(name, member_type)