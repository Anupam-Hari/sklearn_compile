from pathlib import Path
import traceback

from parser.python_parser import parse_python_file
from parser.cython_parser import parse_cython_file
from parser.cython_pxd_parser import parse_cython_pxd


SKLEARN_TREE = Path(
    "/home/anupam/Anupam/sklearn_compile/sklearn/tree"
)


def test_python_parser(path: Path):

    tree = parse_python_file(path)

    return type(tree).__name__


def test_cython_parser(path: Path):

    tree = parse_cython_file(path)

    return type(tree).__name__


def test_pxd_parser(path: Path):

    tree = parse_cython_pxd(path)

    return type(tree).__name__


def main():

    passed = []
    failed = []

    files = sorted(
        file
        for file in SKLEARN_TREE.rglob("*")
        if file.suffix in {".py", ".pyx", ".pxd"}
    )

    for file in files:

        try:

            if file.suffix == ".py":

                node_type = test_python_parser(file)

            elif file.suffix == ".pyx":

                node_type = test_cython_parser(file)

            elif file.suffix == ".pxd":

                node_type = test_pxd_parser(file)

            else:

                continue

            passed.append((file, node_type))

        except Exception:

            failed.append(
                (
                    file,
                    traceback.format_exc(),
                )
            )

    print("\n=== PASSED ===\n")

    for file, node_type in passed:

        print(f"{file} -> {node_type}")

    print(f"\nTotal passed: {len(passed)}")

    print("\n=== FAILED ===\n")

    for file, error in failed:

        print(file)

        print(error)

    print(f"Total failed: {len(failed)}")


if __name__ == "__main__":

    main()