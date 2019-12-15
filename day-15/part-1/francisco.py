from tool.runners.python import SubmissionPy


from copy import deepcopy
from collections import defaultdict, deque


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


WALL, OK, OXYGEN = 0, 1, 2
NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
DIRECTIONS = {NORTH: (-1, 0), SOUTH: (1, 0), WEST: (0, -1), EAST: (0, 1)}
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}


def compute_next_position(position, direction):
    return tuple(pos + delta for (pos, delta) in zip(position, DIRECTIONS[direction]))


def show(walls):
    min_X, max_X = min(e[0] for e in walls), max(e[0] for e in walls)
    min_Y, max_Y = min(e[1] for e in walls), max(e[1] for e in walls)

    return "\n".join(
        "".join("#" if (X, Y) in walls else " " for Y in range(min_Y, max_Y + 1))
        for X in range(min_X, max_X + 1)
    )


def solve_part1(program):
    q = deque([(0, (0, 0), IntCodeVM(program))])
    seen = {(0, 0)}
    while q:
        distance, position, vm = q.popleft()

        valid_next_directions = []

        # try to make steps in all directions
        for direction in DIRECTIONS:
            next_pos = compute_next_position(position, direction)
            if next_pos in seen:
                continue

            output = vm.run([direction])
            assert len(output) == 1
            status_code = output[0]
            assert status_code in [WALL, OK, OXYGEN]

            if status_code == OXYGEN:
                return distance + 1

            seen.add(next_pos)

            # step was successful, keep that in mind and go back to previous position
            if status_code != WALL:
                valid_next_directions.append(direction)
                output = vm.run([OPPOSITE[direction]])
                assert output == [OK]

        for i, direction in enumerate(valid_next_directions):
            # duplicate the vm only if there are more than one valid next directions
            vm_ = vm.copy() if i < len(valid_next_directions) - 1 else vm
            output = vm_.run([direction])
            assert output == [OK]
            q.append((distance + 1, compute_next_position(position, direction), vm_))


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return solve_part1(program)
