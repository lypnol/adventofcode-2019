from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        s_min, s_max = s.strip().split("-")
        i_min, i_max = int(s_min), int(s_max)

        return sum(1 for i in range(i_min, i_max+1) if meet_criteria2(i))


def meet_criteria2(n):
    d6 = n % 10
    n = n // 10
    d5 = n % 10
    n = n // 10
    d4 = n % 10
    n = n // 10
    d3 = n % 10
    n = n // 10
    d2 = n % 10
    n = n // 10
    d1 = n

    if not d1 <= d2 <= d3 <= d4 <= d5 <= d6:
        return False

    # return 2 in collections.Counter((d1, d2, d3, d4, d5, d6)).values()

    counts = dict()
    counts[d1] = counts.get(d1, 0) + 1
    counts[d2] = counts.get(d2, 0) + 1
    counts[d3] = counts.get(d3, 0) + 1
    counts[d4] = counts.get(d4, 0) + 1
    counts[d5] = counts.get(d5, 0) + 1
    counts[d6] = counts.get(d6, 0) + 1

    return 2 in counts.values()
