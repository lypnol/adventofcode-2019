from tool.runners.python import SubmissionPy

import itertools

import numpy as np


def fft_iter_2(l, offset, times=100):
    # Key assumption for part 2
    assert offset > 10000 * len(l) // 2
    # l = np.array([l[i % len(l)] for i in range(offset, 10_000 * len(l))])
    l = np.array(
        list(
            itertools.islice(
                itertools.chain(l[offset % len(l) :], itertools.cycle(l)),
                0,
                10000 * len(l) - offset,
            )
        )
    )
    l = np.flip(l)
    for i in range(times):
        # simplified ftt computation using linear cumulative sum algorithm, because we
        # have:
        #   fft[i] = sum(l[i] for i in range(i, len(l)))
        np.cumsum(l, out=l)
        np.mod(l, 10, out=l)
    l = np.flip(l)
    return l


def solve_part2(l):
    offset = int("".join(str(i) for i in l[:7]))
    return "".join(str(i) for i in fft_iter_2(l, offset)[:8])


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        l = [int(s) for s in s.strip()]
        return solve_part2(l)
