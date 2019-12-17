import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

from tool.runners.python import SubmissionPy

BASE_PATTERN = np.array([0, 1, 0, -1])
N_PHASES = 100


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        x = np.array([int(d) for d in s], dtype=np.int)
        n = len(x)

        F = BASE_PATTERN[
            np.mod(
                np.arange(1, n + 1, dtype=np.int)[:, np.newaxis]
                // np.arange(1, n + 1, dtype=np.int),
                len(BASE_PATTERN),
            ).T
        ]

        for _ in range(N_PHASES):
            x = np.mod(np.abs(F @ x), 10)

        return "".join([str(d) for d in x[:8]])
