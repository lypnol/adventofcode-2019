from tool.runners.python import SubmissionPy
import operator

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        intcodes = [int(i) for i in s.strip().split(",")]
        intcodes[1] = 12
        intcodes[2] = 2

        idx = 0
        while intcodes[idx] != 99:
            operand_1 = intcodes[intcodes[idx+1]]
            operand_2 = intcodes[intcodes[idx+2]]
            output_idx = intcodes[idx+3]
            if intcodes[idx] == 1:
                intcodes[output_idx] = operand_1 + operand_2
            elif intcodes[idx] == 2:
                intcodes[output_idx] = operand_1 * operand_2
            idx += 4
        return intcodes[0]






