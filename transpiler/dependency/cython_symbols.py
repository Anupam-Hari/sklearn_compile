import re
from pathlib import Path

from transpiler.dependency.models import Symbol


CLASS_PATTERN = re.compile(
    r"cdef\s+class\s+([A-Za-z_][A-Za-z0-9_]*)"
)

STRUCT_PATTERN = re.compile(
    r"cdef\s+struct\s+([A-Za-z_][A-Za-z0-9_]*)"
)

FUNCTION_PATTERN = re.compile(
    r"(?:cdef|cpdef)\s+[^\n]*?\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
)


def extract_cython_symbols(
    file_path: Path,
) -> list[Symbol]:

    text = file_path.read_text()

    symbols = []

    for match in CLASS_PATTERN.finditer(text):

        symbols.append(
            Symbol(
                name=match.group(1),
                symbol_type="class",
                file_path=file_path,
                language="cython",
            )
        )

    for match in STRUCT_PATTERN.finditer(text):

        symbols.append(
            Symbol(
                name=match.group(1),
                symbol_type="struct",
                file_path=file_path,
                language="cython",
            )
        )

    for match in FUNCTION_PATTERN.finditer(text):

        symbols.append(
            Symbol(
                name=match.group(1),
                symbol_type="function",
                file_path=file_path,
                language="cython",
            )
        )

    return symbols