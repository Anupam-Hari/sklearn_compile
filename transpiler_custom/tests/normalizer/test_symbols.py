from pathlib import Path

from transpiler_custom.parser.parser import parse_file
from transpiler_custom.normalizer.normalize_symbols import (
    normalize_symbols,
)

path = Path("sklearn/utils/_typedefs.pxd")

tree = parse_file(path)

symbols = normalize_symbols(
    tree=tree,
    source_file=path,
)

for symbol in symbols:

    print(
        symbol.kind,
        symbol.name,
    )