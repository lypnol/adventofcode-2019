from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):

        p = [int(v) for v in s.strip().split(",")]
        pc = 0

        def param(pos):
            mode = (p[pc] // 10**(1+pos)) % 10
            return p[p[pc+pos]] if mode == 0 else p[pc+pos]

        input_value = 1
        output = []

        while True:
            op = p[pc] % 100

            if op == 1:
                p[p[pc + 3]] = param(1) + param(2)
                pc += 4
            elif op == 2:
                p[p[pc + 3]] = param(1) * param(2)
                pc += 4
            elif op == 3:
                p[p[pc + 1]] = input_value
                pc += 2
            elif op == 4:
                output.append(param(1))
                pc += 2
            elif op == 99:
                break
            else:
                raise Exception("Unknown op code")

        return output[-1]
