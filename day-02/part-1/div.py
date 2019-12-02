from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):

    def run(self, s):
        intcode = [int(x) for x in s.split(",")]

        intcode[1] = 12
        intcode[2] = 2

        pos = 0
        while True:
            # halt condition
            if intcode[pos] == 99:
                return intcode[0]

            if intcode[pos] == 1:
                intcode[intcode[pos+3]] = intcode[intcode[pos+1]] + intcode[intcode[pos+2]]
            elif intcode[pos] == 2:
                intcode[intcode[pos+3]] = intcode[intcode[pos+1]] * intcode[intcode[pos+2]]

            pos += 4
