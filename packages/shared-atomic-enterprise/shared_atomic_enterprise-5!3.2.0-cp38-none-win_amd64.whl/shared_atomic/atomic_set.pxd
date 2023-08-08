from shared_atomic.atomic_object_backend cimport atomic_object
from shared_atomic.atomic_object_backend cimport subprocess_reference
from libc.limits cimport ULLONG_MAX


cpdef size_t set_get_int(atomic_set intput_set, subprocess_reference reference) except ?ULLONG_MAX
cpdef void set_set_int(atomic_set intput_set, subprocess_reference reference, size_t integer)
cpdef set set_get_set(atomic_set intput_set, subprocess_reference reference)
cpdef void set_set_set(atomic_set intput_set, subprocess_reference reference, set data) except*
cpdef set set_get_and_set(atomic_set intput_set, subprocess_reference reference, set data)
cpdef set set_compare_and_set_value(atomic_set intput_set, subprocess_reference reference, set i, set n)

cdef class atomic_set(atomic_object):
    cpdef size_t get_int(self) except ?ULLONG_MAX
    cpdef void set_int(self, size_t integer) except*
    cpdef set get_set(self)
    cpdef void set_set(self, set data) except*
    cpdef set set_get_and_set(self, set data)
    cpdef set set_compare_and_set_value(self, set i, set n)
    cpdef void reencode(self, str newencode) except*