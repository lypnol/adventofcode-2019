from tool.runners.python import SubmissionPy


class LudogeSubmission(SubmissionPy):
    def two_equal_digits(self, num):
        st = str(num)
        return len({c for c in st}) < len(st)

    def has_increasing_digits(self, num):
        st = str(num)
        return st == "".join(sorted(st))

    def run(self, s):
        a, b = map(int, s.split("-"))
        return sum(
            1
            for x in range(a, b + 1)
            if self.two_equal_digits(x) and self.has_increasing_digits(x)
        )
