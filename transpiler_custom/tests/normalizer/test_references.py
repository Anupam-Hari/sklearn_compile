from collections import Counter
from pathlib import Path

from transpiler_custom.normalizer.normalize_references import (
    normalize_references,
)
from transpiler_custom.parser.parser import parse_file


reference_counts = Counter()
unique_references = set()
per_file = Counter()

python_success = 0
python_failure = 0

cython_success = 0
cython_failure = 0


for path in Path("sklearn/tree").rglob("*"):

    if path.suffix not in {
        ".py",
        ".pyx",
        ".pxd",
    }:

        continue

    if "tests" in path.parts:

        continue

    try:

        tree = parse_file(path)

        references = normalize_references(
            tree=tree,
            source_file=path,
        )

        for reference in references:

            unique_references.add(
                (
                    reference.kind,
                    reference.name,
                )
            )

            reference_counts[
                reference.kind
            ] += 1

            per_file[
                reference.source_file
            ] += 1


        if path.suffix == ".py":

            python_success += 1

        else:

            cython_success += 1

    except Exception as e:

        print(f"FAILED: {path}")
        print(type(e).__name__)
        print(e)

        if path.suffix == ".py":

            python_failure += 1

        else:

            cython_failure += 1


print("\n=== REFERENCE COUNTS ===\n")

for name, count in sorted(
    reference_counts.items()
):

    print(f"{name}: {count}")


print("\n=== PER-FILE COUNT ===\n")

for path, count in sorted(
    per_file.items()
):

    print(f"{path}: {count}")

print("\n=== UNIQUE REFERENCES ===\n")

for kind, name in sorted(unique_references):

    print(
        f"{kind:<20}"
        f"{name}"
    )

print("\n=== PYTHON ===\n")

print(f"Success: {python_success}")
print(f"Failure: {python_failure}")


print("\n=== CYTHON ===\n")

print(f"Success: {cython_success}")
print(f"Failure: {cython_failure}")