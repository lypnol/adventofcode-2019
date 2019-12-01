from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        return sum(int(v) // 3 - 2 for v in s.splitlines())
