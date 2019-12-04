from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        s_min, s_max = s.strip().split("-")
        i_min, i_max = int(s_min), int(s_max)

        return sum(1 for i in range(i_min, i_max+1) if meet_criteria(i))


def meet_criteria(n):
    d = n % 10
    n = n // 10

    has_dup = False

    while n > 0:
        dd = n % 10
        n = n // 10
        if dd > d:
            return False
        elif dd == d:
            has_dup = True
        d = dd

    return has_dup


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

    return d1 <= d2 <= d3 <= d4 <= d5 <= d6 and len({d1, d2, d3, d4, d5, d6}) < 6
