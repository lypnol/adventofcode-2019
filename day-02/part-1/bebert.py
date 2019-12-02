from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s: str):
        # s = "1,9,10,3,2,3,11,0,99,30,40,50"
        codes = [int(x) for x in s.split(",")]
        codes[1] = 12
        codes[2] = 2
        i = 0
        while codes[i] != 99:
            if codes[i] == 1:
                codes[codes[i+3]] = codes[codes[i+1]] + codes[codes[i+2]]
            else:
                codes[codes[i+3]] = codes[codes[i+1]] * codes[codes[i+2]]
            i += 4
        return codes[0]
