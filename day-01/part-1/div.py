from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):

    def run(self, s):
        values = (int(x) for x in s.splitlines())
        return sum((x//3-2) for x in values)

