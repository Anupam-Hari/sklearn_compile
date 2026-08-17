from pprint import pprint

from transpiler.agent.tools.mapping_analyzer import (
    analyze_inventory,
)


report = analyze_inventory()

print()

print("=" * 80)

print("TOTAL NODES")

print("=" * 80)

print(len(report))

print()

print("=" * 80)

print("UNMAPPED NODES")

print("=" * 80)

unmapped = [

    node

    for node in report

    if not node["mapped"]

]

print(

    f"Unmapped nodes: {len(unmapped)}"

)

for node in unmapped:

    print(

        f'{node["language"]}: {node["node"]}'

    )