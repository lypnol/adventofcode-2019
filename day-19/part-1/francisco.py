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


def solve_part1(program, limit=50):
    return sum(status(x, y, program) for x in range(limit) for y in range(limit))


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return solve_part1(program)
