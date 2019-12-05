from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def has_required_properties(self, n):
        digits = list(str(n))
        last_digit = digits[0]
        same_adjacent_digit = False
        for d in digits[1:]:
            if d < last_digit:
                return False
            if d == last_digit:
                same_adjacent_digit = True

            last_digit = d

        return same_adjacent_digit

    def run(self, s):
        lower, upper = [int(v) for v in s.split("-")]

        sol = 0
        for n in range(lower, upper + 1):
            if self.has_required_properties(n):
                sol += 1
        return sol
