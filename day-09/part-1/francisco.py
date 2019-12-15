from tool.runners.python import SubmissionPy


import copy
from collections import defaultdict


def execute(program, input_):
    program = defaultdict(lambda: 0, {i: e for i, e in enumerate(program)})
    i = 0
    j = 0
    relative_base = 0
    output = []
    while program[i] != 99:
        opcode = program[i] % 100
        assert 1 <= opcode <= 9

        modes = {
            1: (program[i] // 100) % 10,
            2: (program[i] // 1000) % 10,
            3: (program[i] // 10000) % 10,
        }

        def param(n):
            if modes[n] == 0:
                return program[program[i + n]]
            elif modes[n] == 1:
                return program[i + n]
            elif modes[n] == 2:
                return program[program[i + n] + relative_base]
            else:
                assert False

        def param_addr(n):
            if modes[n] == 0:
                return program[i + n]
            elif modes[n] == 2:
                return program[i + n] + relative_base
            else:
                assert False

        if opcode == 1:  # plus
            program[param_addr(3)] = param(1) + param(2)
            i += 4
        elif opcode == 2:  # mul
            program[param_addr(3)] = param(1) * param(2)
            i += 4
        elif opcode == 3:  # input
            program[param_addr(1)] = input_[j]
            j += 1
            i += 2
        elif opcode == 4:  # output
            output.append(param(1))
            i += 2
        elif opcode == 5:  # jump if true
            if param(1) != 0:
                i = param(2)
            else:
                i += 3
        elif opcode == 6:  #  jump if false
            if param(1) == 0:
                i = param(2)
            else:
                i += 3
        elif opcode == 7:  # less than
            program[param_addr(3)] = 1 if param(1) < param(2) else 0
            i += 4
        elif opcode == 8:  # equals
            program[param_addr(3)] = 1 if param(1) == param(2) else 0
            i += 4
        elif opcode == 9:  # relative base update
            relative_base += param(1)
            i += 2
        else:
            assert False
    return output


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return execute(program, [1])[0]
