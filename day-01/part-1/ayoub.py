from tool.runners.python import SubmissionPy


class AyoubSubmission(SubmissionPy):

    def run(self, s):
        return sum([
            (int(l) // 3 - 2) for l in s.strip().split('\n')
        ])
