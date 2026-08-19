from collections import Counter
from pathlib import Path

from parser.cython_pxd_parser import parse_cython_pxd
from parser.cython_pyx_parser import parse_cython_pyx


def collect(node, counter):

    counter[type(node).__name__] += 1

    for child_attr in getattr(node, "child_attrs", ()):

        value = getattr(node, child_attr, None)

        if isinstance(value, list):

            for item in value:

                if hasattr(item, "child_attrs"):

                    collect(item, counter)

        elif hasattr(value, "child_attrs"):

            collect(value, counter)


for path, parser in [
    (
        Path("sklearn/tree/_tree.pxd"),
        parse_cython_pxd,
    ),
    (
        Path("sklearn/tree/_tree.pyx"),
        parse_cython_pyx,
    ),
]:

    counter = Counter()

    tree = parser(path)

    collect(tree, counter)

    print(f"\n=== {path.name} ===")

    for node_type in sorted(counter):

        print(
            f"{node_type:30} {counter[node_type]}"
        )