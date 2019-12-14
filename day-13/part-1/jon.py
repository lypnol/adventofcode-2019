from tool.runners.python import SubmissionPy
import collections


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]

        screen = {}
        computer = compute(code, 0)

        try:
            while True:
                x = next(computer)
                y = next(computer)
                v = next(computer)
                screen[(x, y)] = v
        except StopIteration:
            pass

        return sum(1 for v in screen.values() if v == 2)


def compute(code, input_value):
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
            p[index(1)] = input_value
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
