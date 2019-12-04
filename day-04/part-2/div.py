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
        # and only two
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1

            if j-i == 2:
                return True

            i = j

        return False

    def run(self, s):
        min_value, max_value = [int(x) for x in s.split("-")]
        return sum(1 for x in range(min_value, max_value+1) if self.match(x))
