from itertools import chain, repeat, islice, cycle
import numpy as np

from tool.runners.python import SubmissionPy

N_PHASES = 100
N_REPETITIONS = 10_000


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        offset = int(s[:7])
        assert offset > N_REPETITIONS * len(s) // 2

        signal = [int(d) for d in s]
        signal = islice(
            chain(islice(signal, offset % len(s), len(s)), cycle(signal)),
            0,
            len(s) * N_REPETITIONS - offset,
        )
        signal = np.flip(np.array(list(signal), dtype=np.int))

        for k in range(N_PHASES):
            np.cumsum(signal, out=signal)
            if k % 3 == 1:  # HACK: min number of mod to prevent int overflows
                np.mod(signal, 10, out=signal)

        return "".join([str(d % 10) for d in signal[-8:][::-1]])

