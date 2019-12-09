import itertools
from tool.runners.python import SubmissionPy


def method_args(method):
    return len(method.__code__.co_varnames) - 1


class Program(object):
    def __init__(self, code, inp):
        self.inp = inp
        self.out = []
        self.code = code
        self.code.extend([0 for _ in range(10 * len(code))])
        self.rel_base = 0

    def op_add(self, a, b, c):
        self.code[c] = self.code[a] + self.code[b]

    def op_mul(self, a, b, c):
        self.code[c] = self.code[a] * self.code[b]

    def op_inp(self, a):
        self.code[a] = self.inp.pop(0)

    def op_out(self, a):
        self.out.append(self.code[a])

    def jump_if_true(self, a, b):
        if self.code[a] != 0:
            return self.code[b]

    def jump_if_false(self, a, b):
        if self.code[a] == 0:
            return self.code[b]

    def less_than(self, a, b, c):
        self.code[c] = int(self.code[a] < self.code[b])

    def equals(self, a, b, c):
        self.code[c] = int(self.code[a] == self.code[b])

    def adjust_rel_base(self, a):
        self.rel_base += self.code[a]

    def pointers(self, pc, modes):
        for i in itertools.count():
            p = self.code[pc + 1 + i]
            mode = modes % 10

            if mode == 0:
                yield p
            elif mode == 1:
                yield pc + 1 + i
            elif mode == 2:
                yield p + self.rel_base
            else:
                raise ValueError(f"invalid mode: {mode}")

            modes //= 10

    def opcodes(self):
        return [
            (method_args(meth), meth)
            for meth in [
                self.op_add,
                self.op_mul,
                self.op_inp,
                self.op_out,
                self.jump_if_true,
                self.jump_if_false,
                self.less_than,
                self.equals,
                self.adjust_rel_base,
            ]
        ]

    def run(self):
        # operands, func
        opcodes = self.opcodes()
        STOP = 99

        pc = 0

        while True:
            opcode = self.code[pc]
            instr, mode = opcode % 100, opcode // 100

            if opcode == STOP:
                return self.out

            n_args, func = opcodes[instr - 1]

            args = list(itertools.islice(self.pointers(pc, mode), n_args))

            new_pc = func(*args)
            if new_pc is not None:
                pc = new_pc
            else:
                pc += n_args + 1


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        code = [int(i) for i in s.split(",")]
        return Program(code, [2]).run()[0]
