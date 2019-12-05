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
    in_matching_digits_group = False

    previous_d = n_str[0]
    for d in n_str[1:]:
        if previous_d > d:
            return False
        
        if d == previous_d and in_matching_digits_group:
            # more than 2 duplicated digits
            has_dup = False
        elif not has_dup and previous_d == d:
            # not meet cond yet and 2 duplicated digits
            has_dup = True
            in_matching_digits_group = True
        else:
            in_matching_digits_group = False
        previous_d = d
    return has_dup
