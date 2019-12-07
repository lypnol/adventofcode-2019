from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def has_required_properties(self, n):
        digits = list(str(n))
        last_digit = digits[0]
        same_digit = 1
        same_2_digit = False
        for d in digits[1:]:
            if d < last_digit:
                return False
            if d == last_digit:
                same_digit += 1
            else:
                if same_digit == 2:
                    same_2_digit = True
                same_digit = 1

            last_digit = d

        return same_2_digit or same_digit == 2

    def run(self, s):
        lower, upper = [int(v) for v in s.split("-")]

        sol = 0
        for n in range(lower, upper + 1):
            if self.has_required_properties(n):
                sol += 1
        return sol
