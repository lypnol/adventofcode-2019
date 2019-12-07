from tool.runners.python import SubmissionPy


class BenterrisSubmission(SubmissionPy):

    def run(self, s):
        t = 0
        for x in s.split("\n"):
            k = int(int(x)/3) - 2
            while k >= 0:
                t += k
                k = int(k/3) -2
        return t

