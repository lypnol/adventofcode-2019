from tool.runners.python import SubmissionPy
import collections


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]

        computers = [Computer(code, [i]) for i in range(50)]

        while True:
            for c in computers:
                out = c.tick()
                if out is not None:
                    a, x, y = out
                    if a == 255:
                        return y
                    inputs = computers[a].inputs
                    inputs.append(x)
                    inputs.append(y)


class Computer:

    def __init__(self, code, inputs):
        self.p = collections.defaultdict(int, enumerate(code))
        self.pc = 0
        self.relative_base = 0
        self.inputs = collections.deque(inputs)
        self.out_tmp = []

    def addr(self, pos):
        mode = (self.p[self.pc] // 10 ** (1 + pos)) % 10
        if mode == 0:
            return self.p[self.pc + pos]
        if mode == 1:
            return self.pc + pos
        if mode == 2:
            return self.relative_base + self.p[self.pc + pos]
        raise Exception("Bad param mode")

    def tick(self):
        p = self.p
        addr = self.addr

        op = p[self.pc] % 100

        if op == 1:
            p[addr(3)] = p[addr(1)] + p[addr(2)]
            self.pc += 4
        elif op == 2:
            p[addr(3)] = p[addr(1)] * p[addr(2)]
            self.pc += 4
        elif op == 3:
            p[addr(1)] = self.inputs.popleft() if len(self.inputs) > 0 else -1
            self.pc += 2
        elif op == 4:
            self.out_tmp.append(p[addr(1)])
            self.pc += 2
            if len(self.out_tmp) == 3:
                packet = self.out_tmp
                self.out_tmp = []
                return packet
        elif op == 5:
            self.pc = p[addr(2)] if p[addr(1)] != 0 else self.pc + 3
        elif op == 6:
            self.pc = p[addr(2)] if p[addr(1)] == 0 else self.pc + 3
        elif op == 7:
            p[addr(3)] = 1 if p[addr(1)] < p[addr(2)] else 0
            self.pc += 4
        elif op == 8:
            p[addr(3)] = 1 if p[addr(1)] == p[addr(2)] else 0
            self.pc += 4
        elif op == 9:
            self.relative_base += p[addr(1)]
            self.pc += 2
        elif op == 99:
            pass
        else:
            raise Exception("Unknown op code")

        return None
