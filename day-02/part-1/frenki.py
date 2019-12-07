from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        v = list(map(int, s.split(',')))
        i = 0
        v[1], v[2] = 12,2
        while v[i] != 99:
            i1 = v[i+1]
            i2 = v[i+2]
            i3 = v[i+3]
            if v[i] == 2:
                res = v[i1] * v[i2]
            else:
                res = v[i1] + v[i2]
            v[i3] = res
            i += 4
        return v[0]
