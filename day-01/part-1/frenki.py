from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        return sum(int(i)//3 - 2 for i in s.splitlines())