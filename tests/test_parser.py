from pathlib import Path

from transpiler.parser.cython_parser import parse_cython_file


path = Path("sklearn/tree/_tree.pxd")

lines = path.read_text().splitlines()

for i, line in enumerate(lines, 1):

    print(f"{i:4}: {line}")

tree = parse_cython_file(path)

print(type(tree).__name__)