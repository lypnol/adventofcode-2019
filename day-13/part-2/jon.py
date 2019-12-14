from tool.runners.python import SubmissionPy
import collections
import time


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]
        code[0] = 2
        verbose = False

        screen = {}
        score = 0
        x_ball = 0
        x_paddle = 0

        def input_func():
            if verbose:
                print("Score: {}".format(score))
                print_screen(screen)
                time.sleep(0.01)
            return 1 if x_ball > x_paddle else -1 if x_ball < x_paddle else 0

        computer = compute(code, input_func)

        try:
            while True:
                pos = (next(computer), next(computer))
                v = next(computer)
                if verbose:
                    screen[pos] = v
                if v == 4:
                    x_ball = pos[0]
                elif v == 3:
                    x_paddle = pos[0]
                if pos == (-1, 0):
                    score = v
        except StopIteration:
            pass

        return score


tile_repr = {
    0: " ",
    1: "|",
    2: "#",
    3: "-",
    4: "o",
}


def print_screen(screen):
    w = max(x for x, _ in screen) + 1
    h = max(y for _, y in screen) + 1
    lines = [[" "]*w for _ in range(h)]

    for (x, y), v in screen.items():
        lines[y][x] = tile_repr[v]

    for l in lines:
        print("".join(l))


def compute(code, input_func):
    p = collections.defaultdict(int, enumerate(code))
    pc = 0
    relative_base = 0

    def index(pos):
        mode = (p[pc] // 10 ** (1 + pos)) % 10
        if mode == 0:
            return p[pc + pos]
        if mode == 1:
            return pc + pos
        if mode == 2:
            return relative_base + p[pc + pos]
        raise Exception("Bad param mode")

    while True:
        op = p[pc] % 100

        if op == 1:
            p[index(3)] = p[index(1)] + p[index(2)]
            pc += 4
        elif op == 2:
            p[index(3)] = p[index(1)] * p[index(2)]
            pc += 4
        elif op == 3:
            p[index(1)] = input_func()
            pc += 2
        elif op == 4:
            yield p[index(1)]
            pc += 2
        elif op == 5:
            pc = p[index(2)] if p[index(1)] != 0 else pc + 3
        elif op == 6:
            pc = p[index(2)] if p[index(1)] == 0 else pc + 3
        elif op == 7:
            p[index(3)] = 1 if p[index(1)] < p[index(2)] else 0
            pc += 4
        elif op == 8:
            p[index(3)] = 1 if p[index(1)] == p[index(2)] else 0
            pc += 4
        elif op == 9:
            relative_base += p[index(1)]
            pc += 2
        elif op == 99:
            break
        else:
            raise Exception("Unknown op code")
