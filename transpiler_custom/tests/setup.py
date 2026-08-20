from setuptools import Extension
from setuptools import setup

from Cython.Build import cythonize

import numpy as np

extensions = [
    Extension(
        "sklearn.tree._tree",
        ["sklearn/tree/_tree.pyx"],
        include_dirs=[np.get_include()],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        language_level=3,
    )
)