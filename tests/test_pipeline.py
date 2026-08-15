from pathlib import Path

from transpiler.pipeline.dependency_pipeline import (
    build_dependency_pipeline,
)

build_dependency_pipeline(
    Path("sklearn")
)