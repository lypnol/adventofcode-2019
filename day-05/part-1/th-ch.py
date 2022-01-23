from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        program = list(map(int, s.split(",")))
        i = 0
        last_output = None
        while True:
            instruction = str(program[i])
            opcode = int(instruction[-2:])
            if opcode == 99:
                return last_output

            modes = instruction[:-2].zfill(3)

            if opcode == 3:
                program[program[i + 1]] = 1  # input
                i += 2
            elif opcode == 4:
                last_output = (
                    program[program[i + 1]] if modes[2] == "0" else program[i + 1]
                )
                i += 2
            else:
                parameter1 = (
                    program[program[i + 1]] if modes[2] == "0" else program[i + 1]
                )
                parameter2 = (
                    program[program[i + 2]] if modes[1] == "0" else program[i + 2]
                )
                if opcode == 1:
                    value = parameter1 + parameter2
                elif opcode == 2:
                    value = parameter1 * parameter2
                program[program[i + 3]] = value
                i += 4
