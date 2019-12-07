from tool.runners.python import SubmissionPy
import itertools 

class SilvestreSubmission(SubmissionPy):


    def run(self, s):
        intcodes = [int(i) for i in s.strip().split(",")]

        max_output = 0
        for phase_settings in itertools.permutations(range(5, 10), 5):
            # initialization
            states = {
                i: {
                  "intcodes": intcodes.copy(),
                  "idx": 0,
                  "inputs": [phase_settings[i]] if i != 0 else [phase_settings[i], 0],
                  "outputs": [],
                  "is_finished": False 
                } for i in range(5)
            }

            # main computation
            current_idx = 0
            for _ in range(10_000):
                states[current_idx] = self.compute(states[current_idx])
                next_idx = current_idx+1 if current_idx < 4 else 0
                states[next_idx]["inputs"] += states[current_idx]["outputs"]
                if states[4]["is_finished"]:
                    break
                else:
                    states[current_idx]["outputs"] = []
                    current_idx = next_idx            
            max_output = max(max_output, states[4]["outputs"][-1])
        return max_output

    @staticmethod
    def compute(state):
        intcodes = state["intcodes"]
        idx = state["idx"]
        inputs = state["inputs"]
        outputs = state["outputs"]
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
                outputs.append(last_output)
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
                if inputs:
                    intcodes[output_idx] = inputs.pop(0)
                else:
                    return {
                        "intcodes": intcodes,
                        "idx": idx,
                        "inputs": inputs,
                        "outputs": outputs,
                        "is_finished": False
                    }
            elif opcode == 4:
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
                return {
                        "intcodes": intcodes,
                        "idx": idx,
                        "inputs": inputs,
                        "outputs": outputs,
                        "is_finished": True
                    }
            else:
                raise NotImplementedError
            idx += len(modes) + 1
        return -1

