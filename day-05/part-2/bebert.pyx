cdef int get_param(int[] codes, int index, int mode):
    if mode == 0:  # position mode
        return codes[codes[index]]
    else:
        return codes[index]  # immediate mode


cpdef int run(str s):
    # s = "1,9,10,3,2,3,11,0,99,30,40,50"
    # s = "1,9,10,3,2,3,11,0,99,-20,40,50"
    # s = "3,13,004,1,1,9,10,3,2,3,11,0,99,-20,40,50"

    cdef int i, step, inp, out, op_code, tmp1, tmp2
    cdef str x

    cdef int LEN_CODE = 1000
    cdef int[1000] codes
    for i in range(LEN_CODE):
        codes[i] = 0

    cdef int[3] modes
    for i in range(3):
        modes[i] = 0

    for i, x in enumerate(s.split(",")):
        codes[i] = int(x)

    inp = 5
    out = 0

    i = 0
    op_code = codes[i] % 100
    modes[0] = codes[i] // 100 % 10
    modes[1] = codes[i] // 1000 % 10
    # modes[2] = codes[i] // 10000 % 10

    while op_code != 99:

        if op_code == 1:
            step = 4
            tmp1 = get_param(codes, i+1, modes[0])
            tmp2 = get_param(codes, i+2, modes[1])
            codes[codes[i+3]] = tmp1 + tmp2

        elif op_code == 2:
            step = 4
            tmp1 = get_param(codes, i+1, modes[0])
            tmp2 = get_param(codes, i+2, modes[1])
            codes[codes[i+3]] = tmp1 * tmp2

        elif op_code == 3:
            step = 2
            codes[codes[i+1]] = inp

        elif op_code == 4:
            step = 2
            out = get_param(codes, i+1, modes[0])

        elif op_code == 5:
            step = 3
            tmp1 = get_param(codes, i+1, modes[0])
            if tmp1 != 0:
                step = 0
                i = get_param(codes, i+2, modes[1])

        elif op_code == 6:
            step = 3
            tmp1 = get_param(codes, i+1, modes[0])
            if tmp1 == 0:
                i = get_param(codes, i+2, modes[1])
                step = 0

        elif op_code == 7:
            step = 4
            tmp1 = get_param(codes, i+1, modes[0])
            tmp2 = get_param(codes, i+2, modes[1])
            if tmp1 < tmp2:
                codes[codes[i+3]] = 1
            else:
                codes[codes[i+3]] = 0

        elif op_code == 8:
            step = 4
            tmp1 = get_param(codes, i+1, modes[0])
            tmp2 = get_param(codes, i+2, modes[1])
            if tmp1 == tmp2:
                codes[codes[i+3]] = 1
            else:
                codes[codes[i+3]] = 0

        i += step
        op_code = codes[i] % 100
        modes[0] = codes[i] // 100 % 10
        modes[1] = codes[i] // 1000 % 10
        # modes[2] = codes[i] // 10000 % 10

    return out
