from tool.runners.python import SubmissionPy


class AyoubSubmission(SubmissionPy):

    def _check(self, n):
        s = str(n)
        found = False
        for i in range(1, len(s)):
            if s[i] < s[i-1]:
                return False
            if s[i] == s[i-1]:
                found = True
        return found

    def run(self, s):
        a, b = map(int, s.split('-'))
        c = 0
        for n in range(a, b+1):
            if self._check(n):
                c += 1
        return c
