from tool.runners.python import SubmissionPy


class Submission(SubmissionPy):
    def run(self, s):
        return sum(int(m) // 3 - 2 for m in s.split("\n"))

