from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def execute(self, p, input1, input2):
        p[1] = input1
        p[2] = input2
        pc = 0
        while True:
            opcode = p[pc]
            if opcode == 1:
                a = p[p[pc + 1]]
                b = p[p[pc + 2]]
                p[p[pc + 3]] = a + b

            elif opcode == 2:
                a = p[p[pc + 1]]
                b = p[p[pc + 2]]
                p[p[pc + 3]] = a * b

            elif opcode == 99:
                break
            pc += 4

        return p[0]

    def run(self, s):
        p = [int(n) for n in s.split(",")]

        for noun in range(100):
            for verb in range(100):
                res = self.execute(p.copy(), noun, verb)
                if res == 19690720:
                    return 100 * noun + verb

        return 0
