from tool.runners.python import SubmissionPy

class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        v2 = list(map(int, s.split(',')))
        for k in range(100):
            for j in range(100):
                v = v2.copy()
                v[1], v[2] = k,j
                i = 0
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
                if v[0] == 19690720 :
                    return 100 * k + j
