from pathlib import Path
import json

def read_file(path):

    return Path(path).read_text(
        encoding="utf-8",
    )


def write_file(path, content):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content,
        encoding="utf-8",
    )



def read_json(path):

    return json.loads(

        Path(path).read_text(
            encoding="utf-8",
        )

    )


def write_json(path, data):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(

        json.dumps(
            data,
            indent=4,
        ),

        encoding="utf-8",

    )