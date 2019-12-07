import itertools
from tool.runners.python import SubmissionPy


class Program(object):
    def __init__(self, code, inp):
        self.inp = inp
        self.out = []
        self.code = code

    def op_add(self, args):
        self.code[args[2]] = args[1] + args[0]

    def op_mul(self, args):
        self.code[args[2]] = args[1] * args[0]

    def op_inp(self, args):
        self.code[args[0]] = self.inp.pop(0)

    def op_out(self, args):
        self.out.append(args[0])

    def jump_if_true(self, args):
        if args[0] != 0:
            return args[1]

    def jump_if_false(self, args):
        if args[0] == 0:
            return args[1]

    def less_than(self, args):
        self.code[args[2]] = int(args[0] < args[1])

    def equals(self, args):
        self.code[args[2]] = int(args[0] == args[1])

    def params(self, pc, modes, pos=None):
        # overkill to avoid recomputing 1, 10, 100
        for i, mask in enumerate([1, 10, 100]):
            p = self.code[pc + i + 1]
            if modes & mask or pos == i + 1:
                yield p
            else:
                yield self.code[p]

    def run(self):
        # operands, func, optional non immediate arg
        opcodes = [
            (3, self.op_add, 3),
            (3, self.op_mul, 3),
            (1, self.op_inp, 1),
            (1, self.op_out, None),
            (2, self.jump_if_true, None),
            (2, self.jump_if_false, None),
            (3, self.less_than, 3),
            (3, self.equals, 3),
        ]
        STOP = 99

        pc = 0

        while True:
            opcode = self.code[pc]

            if opcode == STOP:
                return self.out[-1]

            n_args, func, pos = opcodes[(opcode % 100) - 1]

            args = list(
                itertools.islice(self.params(pc, opcode // 100, pos=pos), n_args)
            )

            new_pc = func(args)
            if new_pc is not None:
                pc = new_pc
            else:
                pc += n_args + 1


def run_amplifiers(code, phases):
    # First input
    out = 0
    for i, phase in enumerate(phases):
        out = Program(code.copy(), [phase, out]).run()

    return out


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        code = [int(i) for i in s.split(",")]


        return max(
            run_amplifiers(code, phases)
            for phases in itertools.permutations([0, 1, 2, 3, 4])
        )
