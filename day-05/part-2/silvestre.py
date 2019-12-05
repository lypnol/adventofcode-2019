from tool.runners.python import SubmissionPy

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        intcodes = [int(i) for i in s.strip().split(",")]
        return self.compute_output(intcodes)

    def compute_output(self, intcodes):
        last_output = None
        idx = 0
        while True:
            opcode_w_modes = str(intcodes[idx])
            opcode = int(opcode_w_modes[-2:])
            if opcode in [1, 2, 7, 8]:
                modes = opcode_w_modes[:-2].rjust(3, "0")
                operand_1 = intcodes[intcodes[idx+1]] if modes[-1] == "0" else intcodes[idx+1]
                operand_2 = intcodes[intcodes[idx+2]] if modes[-2] == "0" else intcodes[idx+2]
                output_idx = intcodes[idx+3]
                assert modes[-3] == "0"
            elif opcode in [4]:               
                modes = opcode_w_modes[:-2].rjust(1, "0")
                last_output = intcodes[intcodes[idx+1]] if modes[-1] == "0" else intcodes[idx+1]
            elif opcode in [3]:               
                assert opcode_w_modes[:-2].rjust(1, "0") == "0"
                modes = ["0"]
                output_idx = intcodes[idx+1]
            elif opcode in [5, 6]:
                modes = opcode_w_modes[:-2].rjust(2, "0")
                operand_1 = intcodes[intcodes[idx+1]] if modes[-1] == "0" else intcodes[idx+1]
                operand_2 = intcodes[intcodes[idx+2]] if modes[-2] == "0" else intcodes[idx+2]
            
            if opcode == 1:
                intcodes[output_idx] = operand_1 + operand_2
            elif opcode == 2:
                intcodes[output_idx] = operand_1 * operand_2
            elif opcode == 3:
                intcodes[output_idx] = 5
            elif opcode == 4:
                #print("output:", last_output)
                pass
            elif opcode == 5:
                if operand_1 != 0:
                    idx = operand_2
                    continue
            elif opcode == 6:
                if operand_1 == 0:
                    idx = operand_2
                    continue
            elif opcode == 7:
                intcodes[output_idx] = int(operand_1 < operand_2)
            elif opcode == 8:
                intcodes[output_idx] = int(operand_1 == operand_2)
            elif opcode == 99:
                return last_output
            else:
                raise NotImplementedError
            idx += len(modes) + 1
        return -1

