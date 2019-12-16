from tool.runners.python import SubmissionPy
import itertools


class RemiSubmission(SubmissionPy):
    def run(self, s):
        inp = [int(i) for i in list(s)] * 10000
        self.offset = int("".join(str(i) for i in inp[:7]))
        inp = inp[self.offset :]
        for _ in range(100):
            for i in range(len(inp) - 2, -1, -1):
                inp[i] += inp[i + 1]

        return "".join([str(i % 10) for i in inp[:8]])
