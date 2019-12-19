from tool.runners.python import SubmissionPy


from copy import deepcopy
from collections import defaultdict


class IntCodeVM:
    def __init__(self, program):
        self.memory = defaultdict(int, {i: elem for i, elem in enumerate(program)})
        self.instr_ptr = 0
        self.relative_base = 0

    @property
    def stopped(self):
        return self.memory[self.instr_ptr] == 99

    def copy(self):
        return deepcopy(self)

    def param_mode(self, n):
        return (self.memory[self.instr_ptr] // 10 ** (n + 1)) % 10

    def param(self, n):
        mode = self.param_mode(n)
        if mode in [0, 2]:
            return self.memory[self.param_addr(n)]
        elif mode == 1:
            return self.memory[self.instr_ptr + n]
        else:
            raise f"Invalid param mode: {mode}"

    def param_addr(self, n):
        mode = self.param_mode(n)
        if mode == 0:
            return self.memory[self.instr_ptr + n]
        elif mode == 2:
            return self.memory[self.instr_ptr + n] + self.relative_base
        else:
            raise f"Invalid param mode: {modes[n]}"

    def run(self, input_):
        output = []
        input_ptr = 0

        while not self.stopped:
            opcode = self.memory[self.instr_ptr] % 100

            if opcode == 1:  # plus
                self.memory[self.param_addr(3)] = self.param(1) + self.param(2)
                self.instr_ptr += 4
            elif opcode == 2:  # mul
                self.memory[self.param_addr(3)] = self.param(1) * self.param(2)
                self.instr_ptr += 4
            elif opcode == 3:  # input
                # no more inputs: exit at current state
                if input_ptr >= len(input_):
                    return output
                self.memory[self.param_addr(1)] = input_[input_ptr]
                input_ptr += 1
                self.instr_ptr += 2
            elif opcode == 4:  # output
                output.append(self.param(1))
                self.instr_ptr += 2
            elif opcode == 5:  # jump if true
                if self.param(1) != 0:
                    self.instr_ptr = self.param(2)
                else:
                    self.instr_ptr += 3
            elif opcode == 6:  #  jump if false
                if self.param(1) == 0:
                    self.instr_ptr = self.param(2)
                else:
                    self.instr_ptr += 3
            elif opcode == 7:  # less than
                self.memory[self.param_addr(3)] = (
                    1 if self.param(1) < self.param(2) else 0
                )
                self.instr_ptr += 4
            elif opcode == 8:  # equals
                self.memory[self.param_addr(3)] = (
                    1 if self.param(1) == self.param(2) else 0
                )
                self.instr_ptr += 4
            elif opcode == 9:  # relative base update
                self.relative_base += self.param(1)
                self.instr_ptr += 2
            else:
                raise f"Invalid opcode: {opcode}"

        return output


def status(x, y, program):
    vm = IntCodeVM(program)
    output = vm.run([x, y])
    assert len(output) == 1
    return bool(output[0])


def show_beam(program, limit):
    return "\n".join(
        "".join("#" if status(x, y, program) else "." for x in range(limit))
        for y in range(limit)
    )


def beam_limits(program):
    # compute the beam limits by following the edges
    x = 10
    upper = 0
    lower = 0

    while True:
        while not status(x, upper, program):
            upper += 1

        if lower <= upper:
            lower = upper + 1

        while status(x, lower, program):
            lower += 1

        yield x, (lower, upper)

        x += 1


def solve_part2(program, size=100, sanity_check=False):

    limits = dict()
    for x, (lower, upper) in beam_limits(program):
        if sanity_check:
            assert status(x, lower, program) == False
            assert status(x, lower - 1, program) == True
            assert status(x, upper, program) == True
            assert status(x, upper - 1, program) == False

        limits[x] = (lower, upper)
        if x - size in limits:
            # height: lower[x - size + 1] - upper[x]
            if limits[x - size + 1][0] - limits[x][1] >= size:
                return x - size + 1, limits[x][1]


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        x, y = solve_part2(program)
        return x * 10000 + y
