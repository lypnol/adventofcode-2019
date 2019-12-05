from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def run(self, s):
        p = [int(n) for n in s.split(",")]
        pc = 0
        p[1] = 12
        p[2] = 2
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

