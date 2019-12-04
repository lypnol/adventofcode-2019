from tool.runners.python import SubmissionPy


class BenterrisSubmission(SubmissionPy):

    def run(self, s):
        l = [int(x) for x in s.split(",")]
        l[1], l[2], i = 12, 2, 0
        while True:
            if l[i] == 1:
                l[l[i+3]] = l[l[i+2]] + l[l[i+1]]
            elif l[i] == 2:
                l[l[i+3]] = l[l[i+2]] * l[l[i+1]]
            else:
                break
            i += 4
        return l[0]