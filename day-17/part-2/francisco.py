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


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def move(position, direction):
    return tuple(x + y for (x, y) in zip(position, DIRECTIONS[direction]))


def turn_left(direction):
    return (direction - 1) % 4


def turn_right(direction):
    return (direction + 1) % 4


def compress_backtrack(l):
    l = tuple(l)
    dictionary = {}
    compressed = []

    def rec(i):
        if i == len(l):
            return True

        for j in range(i + 2, min(i + 20, len(l) + 1), 2):
            if l[i:j] in dictionary:
                compressed.append(dictionary[l[i:j]])
                if rec(j):
                    return True
                compressed.pop()

            if len(dictionary) < 3 and l[i:j] not in dictionary:
                dictionary[l[i:j]] = len(dictionary)
                compressed.append(dictionary[l[i:j]])
                if rec(j):
                    return True
                compressed.pop()
                del dictionary[l[i:j]]

        return False

    rec(0)

    return sorted(dictionary, key=lambda k: dictionary[k]), compressed


def solve_part2(program, debug=True):
    vm = IntCodeVM(program)
    output = vm.run([])

    max_y = output.index(ord("\n"))
    max_x = len(output) // (max_y + 1)
    get = (
        lambda x, y: output[x * (max_y + 1) + y]
        if 0 <= x < max_x and 0 <= y < max_y
        else ord(".")
    )

    pos = None
    direction = 0

    for x in range(max_x):
        for y in range(max_y):
            if get(x, y) == ord("^"):
                pos = (x, y)

    instructions = []

    while True:
        # try to move forward
        if get(*move(pos, direction)) == ord("#"):
            pos = move(pos, direction)
            if type(instructions[-1]) == int:
                instructions[-1] += 1
            else:
                instructions.append(1)
        # turn left
        elif get(*move(pos, turn_left(direction))) == ord("#"):
            instructions.append("L")
            direction = turn_left(direction)
        # turn right
        elif get(*move(pos, turn_right(direction))) == ord("#"):
            instructions.append("R")
            direction = turn_right(direction)
        # end of the path
        else:
            break

    instructions = [str(s) for s in instructions]
    dictionary, compressed = compress_backtrack(instructions)

    vm = IntCodeVM(program)
    vm.memory[0] = 2
    input_strings = (
        [",".join(chr(ord("A") + s) for s in compressed)]
        + [",".join(word) for word in dictionary]
        + ["n"]
    )
    input_string = "\n".join(input_strings) + "\n"
    output = vm.run([ord(s) for s in input_string])
    return output[-1]


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return solve_part2(program)
