from tool.runners.python import SubmissionPy


def fft_iter_2(l, offset, times=100):
    # Key assumption for part 2
    assert offset > 10000 * len(l) // 2
    l = [l[i % len(l)] for i in range(offset, 10000 * len(l))]
    for i in range(times):
        # simplified ftt computation using linear cumulative sum algorithm, because we
        # have:
        #   fft[i] = sum(l[i] for i in range(i, len(l)))
        for i in reversed(range(len(l) - 1)):
            l[i] += l[i + 1]
        for i in reversed(range(len(l) - 1)):
            l[i] = abs(l[i]) % 10
    return l


def solve_part2(l):
    offset = int("".join(str(i) for i in l[:7]))
    return "".join(str(i) for i in fft_iter_2(l, offset)[:8])


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        l = [int(s) for s in s.strip()]
        return solve_part2(l)
