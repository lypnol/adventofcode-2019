from tool.runners.python import SubmissionPy


class AyoubSubmission(SubmissionPy):

    def run(self, s):
        r = 0
        for l in s.strip().split('\n'):
            f = max(int(l) // 3 - 2, 0)
            r += f
            while f > 0:
                f = max(f // 3 - 2, 0)
                r += f
        return r
