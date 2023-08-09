from shared_atomic.atomic_object_backend cimport atomic_object
from shared_atomic.atomic_object_backend cimport subprocess_reference

cpdef str string_get_string(atomic_string string, subprocess_reference reference)
cpdef void string_set_string(atomic_string string, subprocess_reference reference, str data) except *
cpdef str string_get_and_set(atomic_string string, subprocess_reference reference, str data)
cpdef str string_compare_and_set_value(atomic_string string, subprocess_reference reference, str i, str n)

cdef class atomic_string(atomic_object):
    cdef readonly str x13
    cdef readonly char x14

    cpdef str get_string(self)
    cpdef void set_string(self, str data) except *
    cpdef str string_compare_and_set_value(self, str i, str n)
    cpdef str string_get_and_set(self, str data)
    cpdef void resize(self, char newlength,
                str paddingdirection = *,
                str paddingstr  = *,
                str trimming_direction  = *) except *
    cpdef void reencode(self, str newencode) except*