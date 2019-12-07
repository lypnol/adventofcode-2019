from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]
        return max(result(code, perm) for perm in permutations({5, 6, 7, 8, 9}))


def result(code, perm):
    inputs = [[k] for k in perm]
    inputs[0].append(0)
    computers = [computer(code, i) for i in inputs]
    n = len(computers)

    try:
        while True:
            for i in range(n):
                inputs[(i+1) % n].append(next(computers[i]))
    except StopIteration:
        return inputs[0][-1]


def computer(code, inputs):
    p = code.copy()
    pc = 0

    def param(pos):
        mode = (p[pc] // 10 ** (1 + pos)) % 10
        return p[p[pc + pos]] if mode == 0 else p[pc + pos]

    input_index = 0

    while True:
        op = p[pc] % 100

        if op == 1:
            p[p[pc + 3]] = param(1) + param(2)
            pc += 4
        elif op == 2:
            p[p[pc + 3]] = param(1) * param(2)
            pc += 4
        elif op == 3:
            p[p[pc + 1]] = inputs[input_index]
            input_index += 1
            pc += 2
        elif op == 4:
            yield param(1)
            pc += 2
        elif op == 5:
            pc = param(2) if param(1) != 0 else pc + 3
        elif op == 6:
            pc = param(2) if param(1) == 0 else pc + 3
        elif op == 7:
            p[p[pc + 3]] = 1 if param(1) < param(2) else 0
            pc += 4
        elif op == 8:
            p[p[pc + 3]] = 1 if param(1) == param(2) else 0
            pc += 4
        elif op == 99:
            break
        else:
            raise Exception("Unknown op code")


# Could use itertools.permutations() instead
def permutations(numbers):
    if len(numbers) == 0:
        yield []
        return
    for n in numbers:
        for p in permutations(numbers - {n}):
            p.append(n)
            yield p
