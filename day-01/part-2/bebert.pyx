cpdef int run(s):
    cpdef int total = 0
    cpdef int additional_mass
    cpdef str l

    for l in s.splitlines():
        additional_mass = int(l)
        while additional_mass >= 9:
            additional_mass = additional_mass // 3 - 2
            total += additional_mass
    return total
