from tool.runners.python import SubmissionPy
import itertools
import numpy as np


class RemiSubmission(SubmissionPy):
    def run(self, s):
        offset = int(s[:7])
        inp = np.array([int(i) for i in list(s)])
        inp1 = inp[offset % len(s) :]
        inp = np.flip(
            np.array(
                [
                    i
                    for i in itertools.islice(
                        itertools.chain(inp1, itertools.cycle(inp)),
                        0,
                        len(s) * 10000 - offset,
                    )
                ],
                dtype=np.uint64,
            )
        )
        for j in range(100):
            np.cumsum(inp, out=inp)
            if j % 3 == 0:
                np.mod(inp, 10, out=inp)

        inp = np.flip(inp, axis=0)

        return "".join([str(i) for i in inp[:8]])
