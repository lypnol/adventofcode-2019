from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        intcode = [int(x) for x in s.split(",")]
        intcode[1] = 12
        intcode[2] = 2
        for i in range(0, len(intcode), 4):
            opcode = intcode[i]
            if opcode == 1:
                intcode[intcode[i + 3]] = (intcode[intcode[i + 1]] + intcode[intcode[i + 2]])
            elif opcode == 2:
                intcode[intcode[i + 3]] = (intcode[intcode[i + 1]] * intcode[intcode[i + 2]])
            elif opcode == 99:
                return intcode[0]
            else:
                raise ValueError("Invalid op code")
