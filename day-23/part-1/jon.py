from tool.runners.python import SubmissionPy
import collections


class Found(Exception):
    pass


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]

        inputs = [collections.deque([i]) for i in range(50)]
        waiting = set(range(50))

        def send(packet):
            a, x, y = packet
            if a == 255:
                raise Found(y)
            else:
                inputs[a].append(x)
                inputs[a].append(y)
                waiting.add(a)

        computers = [compute(code, i, send) for i in inputs]

        try:
            while True:
                while waiting:
                    i = waiting.pop()
                    next(computers[i])
                for c in computers:
                    next(c)
        except Found as e:
            return e.args[0]


def compute(code, inputs, send):
    p = collections.defaultdict(int, enumerate(code))
    pc = 0
    relative_base = 0
    packet = []

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
            if len(inputs) == 0:
                yield
            p[index(1)] = inputs.popleft() if len(inputs) > 0 else -1
            pc += 2
        elif op == 4:
            packet.append(p[index(1)])
            if len(packet) == 3:
                send(packet)
                packet = []
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
