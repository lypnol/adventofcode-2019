from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        program = [int(i) for i in s.split(",")]

        program[1] = 12
        program[2] = 2

        pc = 0
        while program[pc] != 99:
            a, b = program[program[pc + 1]], program[program[pc + 2]]
            dest = program[pc + 3]

            if program[pc] == 1:
                program[dest] = a + b
            elif program[pc] == 2:
                program[dest] = a * b
            else:
                raise f"Invalid opcode: {program[pc]}"

            pc += 4
        return program[0]
