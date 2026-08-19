from collections import Counter
from pathlib import Path

from transpiler_custom.normalizer.normalize_symbols import (
    normalize_symbols,
)
from transpiler_custom.parser.parser import parse_file


symbol_counts = Counter()
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

        symbols = normalize_symbols(
            tree=tree,
            source_file=path,
        )

        for symbol in symbols:

            print(
                f"{symbol.kind:<20}"
                f"{symbol.name:<40}"
                f"{symbol.source_file}"
            )

            symbol_counts[symbol.kind] += 1
            per_file[symbol.source_file] += 1

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


print("\n=== SYMBOL COUNTS ===\n")

for name, count in sorted(symbol_counts.items()):

    print(f"{name}: {count}")

print("\n=== PER-FILE COUNT ===\n")

for path, count in sorted(per_file.items()):

    print(f"{path}: {count}")

print("\n=== PYTHON ===\n")

print(f"Success: {python_success}")
print(f"Failure: {python_failure}")

print("\n=== CYTHON ===\n")

print(f"Success: {cython_success}")
print(f"Failure: {cython_failure}")