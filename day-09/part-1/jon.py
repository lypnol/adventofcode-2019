from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]
        return compute(code, [1])


def compute(code, inputs):
    mem = {}
    pc = 0
    relative_base = 0

    def p(i):
        return mem[i] if i in mem else code[i]

    def index(pos):
        mode = (p(pc) // 10 ** (1 + pos)) % 10
        if mode == 0:
            return p(pc + pos)
        if mode == 1:
            return pc + pos
        if mode == 2:
            return relative_base + p(pc + pos)
        raise Exception("Bad param mode")

    def param(pos):
        return p(index(pos))

    input_index = 0
    output_value = None

    while True:
        op = p(pc) % 100

        if op == 1:
            mem[index(3)] = param(1) + param(2)
            pc += 4
        elif op == 2:
            mem[index(3)] = param(1) * param(2)
            pc += 4
        elif op == 3:
            mem[index(1)] = inputs[input_index]
            input_index += 1
            pc += 2
        elif op == 4:
            output_value = param(1)
            pc += 2
        elif op == 5:
            pc = param(2) if param(1) != 0 else pc + 3
        elif op == 6:
            pc = param(2) if param(1) == 0 else pc + 3
        elif op == 7:
            mem[index(3)] = 1 if param(1) < param(2) else 0
            pc += 4
        elif op == 8:
            mem[index(3)] = 1 if param(1) == param(2) else 0
            pc += 4
        elif op == 9:
            relative_base += param(1)
            pc += 2
        elif op == 99:
            break
        else:
            raise Exception("Unknown op code")

    return output_value
