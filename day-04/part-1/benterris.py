from tool.runners.python import SubmissionPy


class BenterrisSubmission(SubmissionPy):

    def run(self, s):
        left, right = s.split("-")
        k = 0
        for x in range(int(left), int(right)):
            if self.is_valid(x):
                k += 1
        return k


    def is_valid(self, n):
        x = [int(i) for i in list(str(n))]
        return (x[0] <= x[1] <= x[2] <= x[3] <= x[4] <= x[5]) and (
            x[0] == x[1] or
            x[1] == x[2] or
            x[2] == x[3] or
            x[3] == x[4] or
            x[4] == x[5]
        )
