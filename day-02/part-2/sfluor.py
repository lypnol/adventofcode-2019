from tool.runners.python import SubmissionPy

def op_add(prog, pc):
    prog[prog[pc+3]] = prog[prog[pc+1]] + prog[prog[pc+2]]
    return 4

def op_mul(prog, pc):
    prog[prog[pc+3]] = prog[prog[pc+1]] * prog[prog[pc+2]]
    return 4

opcodes = (op_add, op_mul)

STOP = 99

def exec_prog(prog, noun, verb):
    # inject noun and verb
    prog[1] = noun
    prog[2] = verb

    pc = 0

    while True:
        opcode = prog[pc]

        if opcode == STOP:
            return prog[0]

        pc += opcodes[opcode - 1](prog, pc)

class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        prog = [int(i) for i in s.split(",")]

        expected = 19690720

        for noun in range(100):
            for verb in range(100):
                # Copy the list
                if exec_prog(prog[:], noun, verb) == expected:
                    return 100 * noun + verb

        print("not found")
        return 0

