INTERNAL_PREFIXES = (
    "splitter.",
    "tree.",
    "builder_stack.",
    "frontier.",
)


def classify_call(call: str) -> str:

    if call.startswith(INTERNAL_PREFIXES):
        return "internal"

    return "external"