import itertools
from tool.runners.python import SubmissionPy


def op_add(prog, args):
    prog[args[2]] = args[1] + args[0]


def op_mul(prog, args):
    prog[args[2]] = args[1] * args[0]


def op_inp(prog, args):
    prog[args[0]] = 1  # fake input


def op_out(prog, args):
    # store the output at the end of the program
    prog[-1] = args[0]

def resolve_params(prog, pc, modes, pos=None):
    # overkill to avoid recomputing 1, 10, 100
    for i, mask in enumerate([1, 10, 100]):
        p = prog[pc + i + 1]
        if modes & mask or pos == i + 1:
            yield p
        else:
            yield prog[p]


# operands, func, optional non immediate arg
opcodes = [
    (3, op_add, 3),
    (3, op_mul, 3),
    (1, op_inp, 1),
    (1, op_out, None),
]
STOP = 99


def exec_prog(prog):
    # Add one element for the output
    prog.append(None)

    pc = 0

    while True:
        opcode = prog[pc]

        if opcode == STOP:
            return prog[-1]

        n_args, func, pos = opcodes[(opcode % 100) - 1]

        args = list(
            itertools.islice(resolve_params(prog, pc, opcode // 100, pos=pos), n_args)
        )

        new_pc = func(prog, args)
        if new_pc is not None:
            pc = new_pc
        else:
            pc += n_args + 1


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        prog = [int(i) for i in s.split(",")]
        return exec_prog(prog)
