from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    @staticmethod
    def run_program(program, noun, verb):
        program[1] = noun
        program[2] = verb

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

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        program = [int(i) for i in s.split(",")]
        target = 19690720

        for noun in range(100):
            for verb in range(100):
                if self.run_program(list(program), noun, verb) == target:
                    return 100 * noun + verb

        return -1
