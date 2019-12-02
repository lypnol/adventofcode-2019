from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):

        program = [int(v) for v in s.strip().split(",")]

        # brute force
        for noun in range(1, 100):
            for verb in range(1, 100):
                if compute(program, noun, verb) == 19690720:
                    return 100 * noun + verb

        raise Exception("not found")


def compute(program, noun, verb):
    p = program.copy()

    p[1] = noun
    p[2] = verb

    pc = 0

    while p[pc] != 99:
        if p[pc] == 1:
            p[p[pc + 3]] = p[p[pc + 1]] + p[p[pc + 2]]
        elif p[pc] == 2:
            p[p[pc + 3]] = p[p[pc + 1]] * p[p[pc + 2]]
        else:
            raise Exception("Unknown op code")
        pc += 4

    return p[0]
