import cython

@cython.cdivision(True)
cpdef int run(s):
    cdef int w = 25
    cdef int h = 6
    cdef int layer_size = 150

    cdef int layer = -1

    cdef int i, j

    cdef int[3] counts
    for j in range(3):
        counts[j] = 151

    cdef int min_zeros = 151
    cdef int min_zeros_result = 0

    cdef str x
    for i, x in enumerate(s):
        if i % layer_size == 0:
            if counts[0] < min_zeros:
                min_zeros = counts[0]
                min_zeros_result = counts[1] * counts[2]
            layer += 1
            for j in range(3):
                counts[j] = 0
        counts[int(x)] += 1

    return min_zeros_result
