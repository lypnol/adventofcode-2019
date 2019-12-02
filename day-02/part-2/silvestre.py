from tool.runners.python import SubmissionPy
import copy

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        intcodes = [int(i) for i in s.strip().split(",")]

        def compute_output(intcodes):
            intcodes = copy.copy(intcodes)
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

        for i in range(0, 100):
            for j in range(0, 100):
                intcodes[1] = i
                intcodes[2] = j
                if compute_output(intcodes) == 19690720:
                    return i * 100 + j