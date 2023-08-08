cdef class atomic_object:
    cdef readonly str mode
    cdef readonly int size
    cdef bint x3
    cdef long x4
    cdef long x5
    cdef int x6
    cdef long long x7
    cdef long long x8


    cdef dict x12
    cpdef void change_mode(self, str newmode=*, bint windows_unix_compatibility=*) except*


cdef class subprocess_reference:
    cdef long long x1
    cdef long long x2

    cpdef void dummy(self)




cdef class multiprocessing_reference(subprocess_reference):
    cdef long long x3
    cdef dict x4

    cdef void close_reference(self, bint windows_unix_compatibility) except *


cpdef subprocess_reference get_reference(atomic_object a)
cpdef void release_reference(subprocess_reference a) except *

