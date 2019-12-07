from tool.runners.python import SubmissionPy

from itertools import permutations


class RemiSubmission(SubmissionPy):
    def run(self, s):
        p = [int(n) for n in s.split(",")]

        m = 0
        for sequence in permutations([5, 6, 7, 8, 9]):

            p_input = 0
            amps = [IntCode(p.copy(), sequence[i]) for i in range(5)]
            while not amps[-1].exited:
                for amp in amps:
                    amp.p_input.append(p_input)
                    amp.execute()
                    p_input = amp.p_output.pop()

            if p_input > m:
                m = p_input

        return m


class IntCode:
    def __init__(self, p, p_input):
        self.p = p
        self.pc = 0
        self.p_input = [p_input]
        self.p_output = []
        self.exited = False

    def get_param(self, p, opcode, index, param):
        modes = opcode // 100
        for _ in range(index):
            modes //= 10
        mode = modes % 10

        if mode == 0:
            return p[param]
        elif mode == 1:
            return param

    def execute(self):
        if self.exited:
            return

        while True:
            opcode = self.p[self.pc]
            if opcode % 100 == 1:
                a = self.get_param(self.p, opcode, 0, self.p[self.pc + 1])
                b = self.get_param(self.p, opcode, 1, self.p[self.pc + 2])
                self.p[self.p[self.pc + 3]] = a + b
                self.pc += 4

            elif opcode % 100 == 2:
                a = self.get_param(self.p, opcode, 0, self.p[self.pc + 1])
                b = self.get_param(self.p, opcode, 1, self.p[self.pc + 2])
                self.p[self.p[self.pc + 3]] = a * b
                self.pc += 4

            elif opcode % 100 == 3:
                try:
                    self.p[self.p[self.pc + 1]] = self.p_input[0]
                    self.p_input = self.p_input[1:]
                except:
                    return
                self.pc += 2

            elif opcode % 100 == 4:
                self.p_output.append(
                    self.get_param(self.p, opcode, 0, self.p[self.pc + 1])
                )
                self.pc += 2

            elif opcode % 100 == 5:
                a = self.get_param(self.p, opcode, 0, self.p[self.pc + 1])
                b = self.get_param(self.p, opcode, 1, self.p[self.pc + 2])
                if a != 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 6:
                a = self.get_param(self.p, opcode, 0, self.p[self.pc + 1])
                b = self.get_param(self.p, opcode, 1, self.p[self.pc + 2])
                if a == 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 7:
                a = self.get_param(self.p, opcode, 0, self.p[self.pc + 1])
                b = self.get_param(self.p, opcode, 1, self.p[self.pc + 2])
                if a < b:
                    self.p[self.p[self.pc + 3]] = 1
                else:
                    self.p[self.p[self.pc + 3]] = 0
                self.pc += 4

            elif opcode % 100 == 8:
                a = self.get_param(self.p, opcode, 0, self.p[self.pc + 1])
                b = self.get_param(self.p, opcode, 1, self.p[self.pc + 2])
                if a == b:
                    self.p[self.p[self.pc + 3]] = 1
                else:
                    self.p[self.p[self.pc + 3]] = 0
                self.pc += 4

            elif opcode % 100 == 99:
                self.exited = True
                break

        return
