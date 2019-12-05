from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def run(self, s):
        sol = 0
        for m in s.split("\n"):
            m = int(m)
            while m > 0:
                m = m // 3 - 2
                if m > 0:
                    sol += m
        return sol
