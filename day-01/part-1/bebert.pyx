cpdef int run(s):
    cpdef int total = 0
    cpdef str l
    for l in s.splitlines():
        total += int(l) // 3 - 2
    return total
