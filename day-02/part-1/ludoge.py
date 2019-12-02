from tool.runners.python import SubmissionPy


class LudogeSubmission(SubmissionPy):
    def run(self, s):
        data = list(map(int, s.split(",")))
        data[1] = 12
        data[2] = 2
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
        return data[0]
