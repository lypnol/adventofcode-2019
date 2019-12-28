from tool.runners.python import SubmissionPy
import itertools
import numpy as np

FINAL_PHASE = 100
REPS = 10000


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        input_ = [int(x) for x in s]
        offset = int(s[:7])
        n = len(input_)
        input_ = np.flip(
            np.array(
                list(itertools.islice(
                    itertools.chain(itertools.islice(input_, offset % n, n), itertools.cycle(input_)),
                    0,
                    n * REPS - offset,
                ))
            )
        )
        for phase in range(FINAL_PHASE):
            input_ = np.cumsum(input_)
            if phase % 3 == 0:
                input_ = np.mod(input_, 10)
        return "".join([str(x) for x in input_[:-9:-1]])
