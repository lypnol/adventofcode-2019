cpdef int run(s):
    # s = "1,9,10,3,2,3,11,0,99,30,40,50"
    cdef LEN_CODE = 200
    cdef int[200] codes
    cdef int i
    cdef str x

    for i, x in enumerate(s.split(",")):
        codes[i] = int(x)

    codes[1] = 12
    codes[2] = 2
    i = 0
    while codes[i] != 99:
        if codes[i] == 1:
            codes[codes[i+3]] = codes[codes[i+1]] + codes[codes[i+2]]
        else:
            codes[codes[i+3]] = codes[codes[i+1]] * codes[codes[i+2]]
        i += 4
    return codes[0]
