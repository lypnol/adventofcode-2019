from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):

    def match(self, x):
        s = str(x)
        n = len(s)

        if n != 6:
            return False

        # always increasing (or equal)
        for i in range(n-1):
            if s[i] > s[i+1]:
                return False

        # should have two identical adjacent digits
        for i in range(n-1):
            if s[i] == s[i+1]:
                return True

        return False

    def run(self, s):
        min_value, max_value = [int(x) for x in s.split("-")]
        return sum(1 for x in range(min_value, max_value+1) if self.match(x))
