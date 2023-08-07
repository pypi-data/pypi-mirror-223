cdef class atomic_object:
    cdef readonly str mode
    cdef readonly int size
    cdef bint x1
    cdef void * x2

    cdef dict x5

    cpdef void change_mode(self, str newmode=*, bint windows_unix_compatibility=*) except *

