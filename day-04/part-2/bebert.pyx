DEF LEN_PW = 6

cdef int check_pw(int[] pw):
    cdef int two_same = 0
    cdef int i
    for i in range(1, LEN_PW):
        if pw[i] < pw[i-1]:
            return 0
        if pw[i] == pw[i-1] and (i < 2 or pw[i-1] != pw[i-2]) and (i == LEN_PW - 1 or pw[i] != pw[i+1]):
            two_same = 1
    return two_same


cdef void increment(int[] pw):
    cdef int i
    for i in range(LEN_PW-1, -1, -1):
        if pw[i] != 9:
            pw[i] += 1
            return
        pw[i] = 0


cpdef int run(s):
    begin_str, end_str = s.strip().split('-')
    cdef int begin = int(begin_str)
    cdef int end = int(end_str)
    cdef int[6] pw = [int(x) for x in begin_str]
    cdef int c = 0
    cdef int i
    for i in range(end - begin + 1):
        c += check_pw(pw)
        increment(pw)
    return c
