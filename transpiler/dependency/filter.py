IGNORED_PREFIXES = {
    "np",
    "copy",
}

IGNORED_METHODS = {
    "append",
    "format",
    "reshape",
    "copy",
    "sum",
    "any",
    "all",
    "sqrt",
    "log2",
    "array",
    "zeros",
    "unique",
    "asarray",
    "ascontiguousarray",
    "flatnonzero",
    "atleast_1d",
    "isin",
    "full",
    "iinfo",
    "deepcopy",
    "sort_indices",
}


def keep_dependency(
    variable: str,
    method: str,
):

    if variable.split(".")[0] in IGNORED_PREFIXES:
        return False

    if method in IGNORED_METHODS:
        return False

    return True