from pathlib import Path

from transpiler.dependency.discover import discover_source_files


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKLEARN_ROOT = PROJECT_ROOT / "sklearn" / "sklearn"


def main():
    files = discover_source_files(SKLEARN_ROOT)

    for file in files:
        print(f"{file.language:8} {file.extension:4} {file.path}")


if __name__ == "__main__":
    main()