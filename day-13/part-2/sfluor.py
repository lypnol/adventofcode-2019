import itertools
import numpy as np
from tool.runners.python import SubmissionPy


def method_args(method):
    return len(method.__code__.co_varnames) - 1


class Program(object):
    def __init__(self, code, inp_func):
        self.inp_func = inp_func
        self.out = None
        self.code = code
        self.code.extend([0 for _ in range(10 * len(code))])
        self.rel_base = 0

    def op_add(self, a, b, c):
        self.code[c] = self.code[a] + self.code[b]

    def op_mul(self, a, b, c):
        self.code[c] = self.code[a] * self.code[b]

    def op_inp(self, a):
        self.code[a] = self.inp_func()

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


def print_tiles(tiles):
    positions = tiles.keys()
    m_x = max(positions, key=lambda p: p[0])[0]
    m_y = max(positions, key=lambda p: p[1])[1]

    trad = [" ", "B", "#", "-", "X"]

    print("\n".join(
        "".join(trad[tiles.get((x, y), 0) for x in range(m_x + 1))
        for y in range(m_y)
    ))


def tiles_to_img(tiles):
    positions = tiles.keys()
    m_x = max(positions, key=lambda p: p[0])[0]
    m_y = max(positions, key=lambda p: p[1])[1] + 10

    trad = [(255, 255, 255), (0, 0, 0), (128, 128, 128), (255, 0, 0), (0, 0, 255)]

    out = []
    for y in range(m_y):
        out.append([trad[tiles.get((x, y), 0)] for x in range(m_x + 1)])

    return np.array(out).astype(np.uint8)


def images_to_video(images):
    import imageio

    imageio.mimsave("/tmp/video.gif", images)


# Directions for the ball
UPR, UPL, DOR, DOL = (1, -1), (-1, -1), (1, 1), (-1, 1)


def direction(old, new):
    if old is None:
        return DOR

    return (new[0] - old[0], new[1] - old[1])


def diff(a, b):
    if a < b:
        return 1
    elif a > b:
        return -1
    else:
        return 0


class State:
    def __init__(self):
        self.ball = None
        self.paddle = None
        self.ball_dir = None

    def move_paddle(self):
        # If ball is going up try to be under the ball
        if self.ball_dir == UPR or self.ball_dir == UPL:
            return diff(self.paddle[0], self.ball[0])

        dy = self.ball[1] - self.paddle[1]
        dx = self.ball[0] - self.paddle[0]

        return diff(0, dx)

    def update(self, x, y, data):
        if data == 3:
            self.paddle = (x, y)
        elif data == 4:
            self.ball_dir = direction(self.ball, (x, y))
            self.ball = (x, y)

    def __repr__(self):
        print(
            f"ball: {self.ball}, paddle: {self.paddle}, ball direction: {self.ball_dir}, center: {self.center}"
        )


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        code = [int(i) for i in s.split(",")]
        code[0] = 2
        state = State()
        prog = Program(code, state.move_paddle)

        buffer = []
        tiles = {}
        scores = []

        # images = []

        for instr in prog.run():
            buffer.append(instr)

            if len(buffer) == 3:
                x, y, data = buffer
                buffer = []

                if x == -1 and y == 0:
                    scores.append(data)
                else:
                    tiles[(x, y)] = data
                    state.update(x, y, data)

                # if data == 4:
                #     images.append(tiles_to_img(tiles))

        # images_to_video(images)
        return scores[-1]
