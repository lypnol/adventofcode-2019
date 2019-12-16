import numpy as np

from tool.runners.python import SubmissionPy

N_PHASES = 100
N_REPETITIONS = 10_000


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        offset = int(s[:7])
        assert offset > len(s) // 2

        signal = [int(d) for d in s] * N_REPETITIONS
        signal = np.array(signal[offset:], dtype=int)[::-1]

        for k in range(N_PHASES):
            np.cumsum(signal, out=signal)
            np.mod(signal, 10, out=signal)

        return "".join([str(d % 10) for d in signal[-8:][::-1]])

