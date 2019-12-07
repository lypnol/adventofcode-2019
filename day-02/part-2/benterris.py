from tool.runners.python import SubmissionPy
import copy

class BenterrisSubmission(SubmissionPy):

    def run(self, s):
        L = [int(x) for x in s.split(",")]
        for x in range(100):
            for y in range(100):
                if self.run_with(x, y, L) == 19690720:
                    return 100 * x + y
        
    def run_with(self, noun, verb, L):
        l = L.copy()
        l[1], l[2], i = noun, verb, 0
        while True:
            if l[i] == 1:
                l[l[i+3]] = l[l[i+2]] + l[l[i+1]]
            elif l[i] == 2:
                l[l[i+3]] = l[l[i+2]] * l[l[i+1]]
            elif l[i] == 99:
                break
            else:
                raise ValueError
            i += 4
        return l[0]

