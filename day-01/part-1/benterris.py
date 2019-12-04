from tool.runners.python import SubmissionPy


class BenterrisSubmission(SubmissionPy):

    def run(self, s):
        return sum([int(int(x)/3) - 2 for x in s.split("\n")])
