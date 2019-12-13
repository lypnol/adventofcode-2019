from tool.runners.python import SubmissionPy

from collections import defaultdict


# XXX: this code should be refactored, but it works and it's not too fun to make
# it look better so I'm not gonna do it

# XXX: this is really ugly, the program should be a class with its own state
def execute(state, input_):
    program, i, j, relative_base = state
    output = []
    while program[i] != 99:
        opcode = program[i] % 100

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
                raise f"Invalid param mode: {modes[n]}"

        def param_addr(n):
            if modes[n] == 0:
                return program[i + n]
            elif modes[n] == 2:
                return program[i + n] + relative_base
            else:
                raise f"Invalid param mode: {modes[n]}"

        if opcode == 1:  # plus
            program[param_addr(3)] = param(1) + param(2)
            i += 4
        elif opcode == 2:  # mul
            program[param_addr(3)] = param(1) * param(2)
            i += 4
        elif opcode == 3:  # input
            # no more inputs: exit at current state
            if j >= len(input_):
                return (program, i, 0, relative_base), output, False
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
            raise f"Invalid opcode: {opcode}"

    return (program, i, 0, relative_base), output, True


def solve_part1(program):
    state = defaultdict(lambda: 0, {i: e for i, e in enumerate(program)}), 0, 0, 0
    state, output, stop = execute(state, [])
    assert stop == True
    assert len(output) % 3 == 0
    return [output[i] for i in range(2, len(output), 3)].count(2)


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return solve_part1(program)
