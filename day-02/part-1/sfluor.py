from tool.runners.python import SubmissionPy

ADD = 1
MUL = 2
STOP = 99

valid_opcodes = {ADD, MUL, STOP}


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here

        prog = [int(i) for i in s.split(",")]

        # Replace some values
        prog[1] = 12
        prog[2] = 2

        pc = 0

        while True:
            opcode = prog[pc]

            if opcode not in valid_opcodes:
                return "invalid opcode"

            if opcode == STOP:
                return prog[0]

            a, b = prog[prog[pc + 1]], prog[prog[pc + 2]]
            ptr = prog[pc + 3]

            if opcode == ADD:
                prog[ptr] = a + b

            if opcode == MUL:
                prog[ptr] = a * b

            pc += 4
