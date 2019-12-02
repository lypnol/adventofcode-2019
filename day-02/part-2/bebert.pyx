cpdef int run(s):
    # s = "1,9,10,3,2,3,11,0,99,30,40,50"
    cdef LEN_CODE = 200
    cdef int[200] codes
    cdef int[200] init_state
    cdef int i, noun, verb
    cdef str x

    for i, x in enumerate(s.split(",")):
        codes[i] = int(x)

    # init_state = codes.copy()
    for i in range(LEN_CODE):
        init_state[i] = codes[i]

    for noun in range(100):
        for verb in range(100):
            # codes = init_state.copy()
            for i in range(LEN_CODE):
                codes[i] = init_state[i]

            codes[1] = noun
            codes[2] = verb
            i = 0
            while codes[i] != 99:
                if codes[i] == 1:
                    codes[codes[i+3]] = codes[codes[i+1]] + codes[codes[i+2]]
                else:
                    codes[codes[i+3]] = codes[codes[i+1]] * codes[codes[i+2]]
                i += 4
            if codes[0] == 19690720:
                return 100 * noun + verb
    return -1
