import re


IGNORE = {
    "if",
    "while",
    "for",
    "with",
    "return",
    "or",
    "and",
    "not",
    "set",
    "build",
    "partition",
    "MemoryError",
}


def extract_calls(source: str) -> list[str]:

    pattern = r"([A-Za-z_][A-Za-z0-9_\.]*)\s*\("

    matches = re.findall(pattern, source)

    return sorted(
        {
            match
            for match in matches
            if match not in IGNORE
        }
    )