from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # s = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        # s = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
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
                program[program[i + 1]] = 5  # input
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
                elif opcode == 5:
                    if parameter1 != 0:
                        i = parameter2
                    else:
                        i += 3
                    continue
                elif opcode == 6:
                    if parameter1 == 0:
                        i = parameter2
                    else:
                        i += 3
                    continue
                elif opcode == 7:
                    value = 1 if parameter1 < parameter2 else 0
                elif opcode == 8:
                    value = 1 if parameter1 == parameter2 else 0

                program[program[i + 3]] = value
                i += 4
