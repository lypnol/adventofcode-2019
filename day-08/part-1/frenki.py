from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        v = 200
        m = 0
        for i in range(len(s)//150):
            r = s.count('0', i*150, (i+1)*150)
            if r < v:
                m = i
                v = r
        r = s.count('1', m*150, (m+1)*150)
        return r*(150-r-v)