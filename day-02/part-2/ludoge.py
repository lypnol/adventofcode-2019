from tool.runners.python import SubmissionPy


class LudogeSubmission(SubmissionPy):
    def run(self, s):
        base_data = list(map(int, s.split(",")))
        for noun in range(100):
            for verb in range(100):
                data = base_data[::]
                data[1] = noun
                data[2] = verb
                i = 0
                while data[i] != 99:
                    opcode, operand_1, operand_2, destination = data[i : i + 4]
                    if opcode == 1:
                        result = data[operand_1] + data[operand_2]
                    elif opcode == 2:
                        result = data[operand_1] * data[operand_2]
                    else:
                        raise Exception(f"Not a valid opcode: {opcode}")
                    data[destination] = result
                    i += 4
                if data[0] == 19690720:
                    return 100 * noun + verb
