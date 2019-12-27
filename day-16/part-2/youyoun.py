from tool.runners.python import SubmissionPy
import numpy as np

BASE_PATTERN = [0, 1, 0, -1]
FINAL_PHASE = 100
PATTERNS = []


def memoize_pattern(pattern):
    PATTERNS.append(pattern)
    return


def get_pattern(n_digit, len_):
    if n_digit < len(PATTERNS):
        return PATTERNS[n_digit]
    pat = []
    i = 0
    while len(pat) < len_ + 1:
        for _ in range(n_digit + 1):
            pat.append(BASE_PATTERN[i])
        i = (i + 1) % len(BASE_PATTERN)
    pat = np.array(pat[1:len_ + 1])
    memoize_pattern(pat)
    return pat


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        input_ = np.array([int(x) for x in s])
        n = len(input_)
        for i in range(n):
            _ = get_pattern(i, n)
        pats = np.array(PATTERNS)
        for phase in range(FINAL_PHASE):
            input_ = np.mod(np.abs(pats @ input_), 10)
        return "".join([str(input_[i]) for i in range(8)])
