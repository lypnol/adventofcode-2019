from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    @staticmethod
    def run_intcode(intcode):
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

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        intcode = [int(x) for x in s.split(",")]
        for noun in range(len(intcode)):
            for verb in range(len(intcode)):
                tmp_intcode = intcode.copy()
                tmp_intcode[1] = noun
                tmp_intcode[2] = verb
                output = YouyounSubmission.run_intcode(tmp_intcode)
                if output == 19690720:
                    return 100 * noun + verb
        return 0
