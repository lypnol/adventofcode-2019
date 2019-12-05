from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        low, high = s.strip().split("-")
        low, high = int(low), int(high)
        return sum(meet_criteria(n) for n in range(low, high+1))

def meet_criteria(n):
    n_str = str(n)
    n = len(n_str)

    if n != 6:
        return False

    has_dup = False
    previous_d = n_str[0]
    for d in n_str[1:]:
        if previous_d > d:
            return False
        elif previous_d == d:
            has_dup=True
        previous_d = d
    return has_dup
    