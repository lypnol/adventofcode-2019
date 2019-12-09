cdef Py_ssize_t permutations[600]
permutations[0:600] = [
    0, 1, 2, 3, 4,
    0, 1, 2, 4, 3,
    0, 1, 3, 2, 4,
    0, 1, 3, 4, 2,
    0, 1, 4, 2, 3,
    0, 1, 4, 3, 2,
    0, 2, 1, 3, 4,
    0, 2, 1, 4, 3,
    0, 2, 3, 1, 4,
    0, 2, 3, 4, 1,
    0, 2, 4, 1, 3,
    0, 2, 4, 3, 1,
    0, 3, 1, 2, 4,
    0, 3, 1, 4, 2,
    0, 3, 2, 1, 4,
    0, 3, 2, 4, 1,
    0, 3, 4, 1, 2,
    0, 3, 4, 2, 1,
    0, 4, 1, 2, 3,
    0, 4, 1, 3, 2,
    0, 4, 2, 1, 3,
    0, 4, 2, 3, 1,
    0, 4, 3, 1, 2,
    0, 4, 3, 2, 1,
    1, 0, 2, 3, 4,
    1, 0, 2, 4, 3,
    1, 0, 3, 2, 4,
    1, 0, 3, 4, 2,
    1, 0, 4, 2, 3,
    1, 0, 4, 3, 2,
    1, 2, 0, 3, 4,
    1, 2, 0, 4, 3,
    1, 2, 3, 0, 4,
    1, 2, 3, 4, 0,
    1, 2, 4, 0, 3,
    1, 2, 4, 3, 0,
    1, 3, 0, 2, 4,
    1, 3, 0, 4, 2,
    1, 3, 2, 0, 4,
    1, 3, 2, 4, 0,
    1, 3, 4, 0, 2,
    1, 3, 4, 2, 0,
    1, 4, 0, 2, 3,
    1, 4, 0, 3, 2,
    1, 4, 2, 0, 3,
    1, 4, 2, 3, 0,
    1, 4, 3, 0, 2,
    1, 4, 3, 2, 0,
    2, 0, 1, 3, 4,
    2, 0, 1, 4, 3,
    2, 0, 3, 1, 4,
    2, 0, 3, 4, 1,
    2, 0, 4, 1, 3,
    2, 0, 4, 3, 1,
    2, 1, 0, 3, 4,
    2, 1, 0, 4, 3,
    2, 1, 3, 0, 4,
    2, 1, 3, 4, 0,
    2, 1, 4, 0, 3,
    2, 1, 4, 3, 0,
    2, 3, 0, 1, 4,
    2, 3, 0, 4, 1,
    2, 3, 1, 0, 4,
    2, 3, 1, 4, 0,
    2, 3, 4, 0, 1,
    2, 3, 4, 1, 0,
    2, 4, 0, 1, 3,
    2, 4, 0, 3, 1,
    2, 4, 1, 0, 3,
    2, 4, 1, 3, 0,
    2, 4, 3, 0, 1,
    2, 4, 3, 1, 0,
    3, 0, 1, 2, 4,
    3, 0, 1, 4, 2,
    3, 0, 2, 1, 4,
    3, 0, 2, 4, 1,
    3, 0, 4, 1, 2,
    3, 0, 4, 2, 1,
    3, 1, 0, 2, 4,
    3, 1, 0, 4, 2,
    3, 1, 2, 0, 4,
    3, 1, 2, 4, 0,
    3, 1, 4, 0, 2,
    3, 1, 4, 2, 0,
    3, 2, 0, 1, 4,
    3, 2, 0, 4, 1,
    3, 2, 1, 0, 4,
    3, 2, 1, 4, 0,
    3, 2, 4, 0, 1,
    3, 2, 4, 1, 0,
    3, 4, 0, 1, 2,
    3, 4, 0, 2, 1,
    3, 4, 1, 0, 2,
    3, 4, 1, 2, 0,
    3, 4, 2, 0, 1,
    3, 4, 2, 1, 0,
    4, 0, 1, 2, 3,
    4, 0, 1, 3, 2,
    4, 0, 2, 1, 3,
    4, 0, 2, 3, 1,
    4, 0, 3, 1, 2,
    4, 0, 3, 2, 1,
    4, 1, 0, 2, 3,
    4, 1, 0, 3, 2,
    4, 1, 2, 0, 3,
    4, 1, 2, 3, 0,
    4, 1, 3, 0, 2,
    4, 1, 3, 2, 0,
    4, 2, 0, 1, 3,
    4, 2, 0, 3, 1,
    4, 2, 1, 0, 3,
    4, 2, 1, 3, 0,
    4, 2, 3, 0, 1,
    4, 2, 3, 1, 0,
    4, 3, 0, 1, 2,
    4, 3, 0, 2, 1,
    4, 3, 1, 0, 2,
    4, 3, 1, 2, 0,
    4, 3, 2, 0, 1,
    4, 3, 2, 1, 0
]


cdef int get_param(int[] codes, int index, int mode):
    if mode == 0:  # position mode
        return codes[codes[index]]
    else:
        return codes[index]  # immediate mode


cpdef int run(str s):
    # s = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    # s = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    # s = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"

    cdef int i, step, op_code, tmp1, tmp2

    cdef int LEN_CODE = 1000
    cdef int[1000] orig_codes
    for i in range(LEN_CODE):
        orig_codes[i] = 0

    cdef str x
    for i, x in enumerate(s.split(",")):
        orig_codes[i] = int(x)

    cdef int[1000] codes

    cdef int[2] modes = [0, 0]

    cdef int[2] inp = [0, 0]
    cdef int inp_cur = 0

    cdef int out = 0
    cdef int max_out = 0

    cdef int perm_cur
    cdef int phase_cur
    for perm_cur in range(120):
        out = 0
        for phase_cur in range(5):
            # Reset
            for i in range(LEN_CODE):
                codes[i] = orig_codes[i]

            inp[0] = permutations[perm_cur * 5 + phase_cur]
            inp[1] = out
            inp_cur = 0

            # ----- Main -----
            i = 0
            op_code = codes[i] % 100
            modes[0] = codes[i] // 100 % 10
            modes[1] = codes[i] // 1000 % 10

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
                    codes[codes[i+1]] = inp[inp_cur]
                    inp_cur += 1

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
            # ===== Main end =====

        if out > max_out:
            max_out = out

    return max_out
