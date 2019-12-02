from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):

        p = [int(v) for v in s.strip().split(",")]

        p[1] = 12
        p[2] = 2

        pc = 0

        while p[pc] != 99:
            if p[pc] == 1:
                p[p[pc+3]] = p[p[pc+1]] + p[p[pc+2]]
            elif p[pc] == 2:
                p[p[pc + 3]] = p[p[pc + 1]] * p[p[pc + 2]]
            else:
                raise Exception("Unknown op code")
            pc += 4

        return p[0]
