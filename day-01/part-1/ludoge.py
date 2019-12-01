from tool.runners.python import SubmissionPy


class LudogeSubmission(SubmissionPy):
    def run(self, s):
        return sum(int(line) // 3 - 2 for line in s.split())
