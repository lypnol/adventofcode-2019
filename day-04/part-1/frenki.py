from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        start, end = s.split('-')
        start = int(start)
        end = int(end)
        res = 0
        for i in range(start, end-1):
            s = str(i)
            r = True
            found = False
            for j in range(5):
                if s[j] > s[j+1]:
                    r = False
                    break
                elif s[j] == s[j+1]:
                    found = True
            if r and found :
                res += 1
        return res