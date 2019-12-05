from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def get_param(self, p, opcode, index, param):
        modes = opcode // 100
        for _ in range(index):
            modes //= 10
        mode = modes % 10

        if mode == 0:
            return p[param]
        elif mode == 1:
            return param

    def execute(self, p, p_input):
        p_output = []
        pc = 0
        while True:
            opcode = p[pc]
            if opcode % 100 == 1:
                a = self.get_param(p, opcode, 0, p[pc + 1])
                b = self.get_param(p, opcode, 1, p[pc + 2])
                p[p[pc + 3]] = a + b
                pc += 4

            elif opcode % 100 == 2:
                a = self.get_param(p, opcode, 0, p[pc + 1])
                b = self.get_param(p, opcode, 1, p[pc + 2])
                p[p[pc + 3]] = a * b
                pc += 4

            elif opcode % 100 == 3:
                p[p[pc + 1]] = p_input
                pc += 2

            elif opcode % 100 == 4:
                p_output.append(self.get_param(p, opcode, 0, p[pc + 1]))
                pc += 2

            elif opcode % 100 == 5:
                a = self.get_param(p, opcode, 0, p[pc + 1])
                b = self.get_param(p, opcode, 1, p[pc + 2])
                if a != 0:
                    pc = b - 3
                pc += 3

            elif opcode % 100 == 6:
                a = self.get_param(p, opcode, 0, p[pc + 1])
                b = self.get_param(p, opcode, 1, p[pc + 2])
                if a == 0:
                    pc = b - 3
                pc += 3

            elif opcode % 100 == 7:
                a = self.get_param(p, opcode, 0, p[pc + 1])
                b = self.get_param(p, opcode, 1, p[pc + 2])
                if a < b:
                    p[p[pc + 3]] = 1
                else:
                    p[p[pc + 3]] = 0
                pc += 4

            elif opcode % 100 == 8:
                a = self.get_param(p, opcode, 0, p[pc + 1])
                b = self.get_param(p, opcode, 1, p[pc + 2])
                if a == b:
                    p[p[pc + 3]] = 1
                else:
                    p[p[pc + 3]] = 0
                pc += 4

            elif opcode % 100 == 99:
                break

        return p_output

    def run(self, s):
        p = [int(n) for n in s.split(",")]

        outputs = self.execute(p.copy(), 5)

        return outputs[-1]
