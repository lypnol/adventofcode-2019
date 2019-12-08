from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        s = s.strip()

        w = 25
        h = 6
        a = w * h
        n = len(s) // a

        def count(v, l):
            return sum(1 for i in range(l*a, (l+1)*a) if s[i] == v)

        _, l0 = min((count("0", l), l) for l in range(n))

        return count("1", l0) * count("2", l0)
