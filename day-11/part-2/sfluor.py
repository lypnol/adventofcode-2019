import itertools
from tool.runners.python import SubmissionPy


def method_args(method):
    return len(method.__code__.co_varnames) - 1


class Program(object):
    def __init__(self, code, inp):
        self.inp = inp
        self.out = None
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
        self.out = self.code[a]

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
        OUT = 4
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

            if instr == OUT:
                yield self.out
                self.out = None


UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        code = [int(i) for i in s.split(",")]
        prog = Program(code, [1])

        buffer = []

        pos = (0, 0)

        painted = {pos: 1}

        direction = UP

        for instr in prog.run():
            buffer.append(instr)

            if len(buffer) == 2:
                color, rotation = buffer

                painted[pos] = color

                direction = (direction + (1 if rotation else -1)) % 4

                if direction == UP:
                    pos = (pos[0], pos[1] + 1)
                elif direction == RIGHT:
                    pos = (pos[0] + 1, pos[1])
                elif direction == DOWN:
                    pos = (pos[0], pos[1] - 1)
                else:
                    pos = (pos[0] - 1, pos[1])

                prog.inp.append(painted.get(pos, 0))
                buffer = []

        rel = [k for k, v in painted.items() if v]
        min_x, _ = min(rel, key=lambda p: p[0])
        _, min_y = min(rel, key=lambda p: p[1])

        points = set([(x - min_x, y - min_y) for (x, y) in rel])

        HEIGHT, WIDTH = 6, 40

        out = []

        for y in range(HEIGHT - 1, -1, -1):
            for x in range(WIDTH):
                out.append(str(int((x, y) in points)))

        return ''.join(out)
