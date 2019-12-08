import cython

@cython.cdivision(True)
cpdef str run(s):
    cdef int w = 25
    cdef int h = 6
    cdef int layer_size = 150

    cdef int i, cur

    cdef int[150] picture
    for cur in range(150):
        picture[cur] = 0

    cdef int layer = -1

    cdef str x
    for i, x in enumerate(s):
        cur = i % layer_size
        if i < layer_size or picture[cur] == 2:
            picture[cur] = int(x)

    # for cur in range(150):
    #     if cur % w == 0:
    #         print(line)
    #         line = ''
    #     line += ' ' if picture[cur] == 0 else '#'
    # print(line)

    cdef str res = ''
    for cur in range(150):
        res += str(picture[cur])
    return res
