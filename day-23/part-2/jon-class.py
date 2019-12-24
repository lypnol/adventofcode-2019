from tool.runners.python import SubmissionPy
import collections


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]

        computers = []
        nat = [0, 0]
        prev_nat_y = None
        waiting = set(range(50))

        def process_output(packet):
            a, x, y = packet
            if a == 255:
                nat[0] = x
                nat[1] = y
                # raise Exception("NAT SET y={}".format(nat[1]))
            else:
                inputs = computers[a].inputs
                inputs.append(x)
                inputs.append(y)
                waiting.add(a)

        computers = [Computer(code, [i], process_output) for i in range(50)]

        while True:
            while waiting:
                while waiting:
                    i = waiting.pop()
                    computers[i].consume()
                for c in computers:
                    c.consume(idle_rounds=1)
            if nat[1] == prev_nat_y:
                return nat[1]
            prev_nat_y = nat[1]
            # print("NAT SEND {}".format(nat))
            process_output((0, nat[0], nat[1]))


class Computer:

    def __init__(self, code, inputs, process_output):
        self.p = collections.defaultdict(int, enumerate(code))
        self.pc = 0
        self.relative_base = 0
        self.inputs = collections.deque(inputs)
        self.out_tmp = []
        self.process_output = process_output

    def addr(self, pos):
        mode = (self.p[self.pc] // 10 ** (1 + pos)) % 10
        if mode == 0:
            return self.p[self.pc + pos]
        if mode == 1:
            return self.pc + pos
        if mode == 2:
            return self.relative_base + self.p[self.pc + pos]
        raise Exception("Bad param mode")

    def consume(self, idle_rounds=0):
        p = self.p
        addr = self.addr

        while True:
            op = p[self.pc] % 100

            if op == 1:
                p[addr(3)] = p[addr(1)] + p[addr(2)]
                self.pc += 4
            elif op == 2:
                p[addr(3)] = p[addr(1)] * p[addr(2)]
                self.pc += 4
            elif op == 3:
                if len(self.inputs) > 0:
                    p[addr(1)] = self.inputs.popleft()
                else:
                    if idle_rounds == 0:
                        return
                    idle_rounds -= 1
                    p[addr(1)] = -1
                self.pc += 2
            elif op == 4:
                self.out_tmp.append(p[addr(1)])
                self.pc += 2
                if len(self.out_tmp) == 3:
                    self.process_output(self.out_tmp)
                    self.out_tmp = []
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
                raise Exception("Computer exited")
            else:
                raise Exception("Unknown op code")
