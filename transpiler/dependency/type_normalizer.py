import re


def normalize_type(type_name: str):

    type_name = type_name.strip()

    type_name = re.sub(
        r"\[.*?\]",
        "",
        type_name,
    )

    type_name = type_name.replace(
        "const ",
        "",
    )

    return type_name.strip()