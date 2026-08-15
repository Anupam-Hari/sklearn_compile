Parser strategy

.py
    ↓
Python AST (built-in ast module)

.pyx
.pxd
.pxi
    ↓
Custom Cython parser

----------------------------------

Python parser responsibilities

- class extraction
- function extraction
- inheritance extraction

----------------------------------

Cython parser responsibilities

- cdef class extraction
- cdef function extraction
- cpdef function extraction
- cdef inline function extraction
- cdef struct extraction
- cdef extern extraction

----------------------------------

Output

NormalizedSymbol