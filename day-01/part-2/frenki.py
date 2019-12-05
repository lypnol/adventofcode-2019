from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self,s):
        r = 0
        for m in s.splitlines():
            s = int(m) // 3 - 2
            while s > 0 :
                r += s
                s = s//3 - 2
        return r
