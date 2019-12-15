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
DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
DELTA = {NORTH: (-1, 0), SOUTH: (1, 0), WEST: (0, -1), EAST: (0, 1)}


def next_position(position, direction):
    return tuple(pos + delta for (pos, delta) in zip(position, DELTA[direction]))


def move(vm, position, direction):
    # XXX: this isn't ideal, we end up spending a lot of time doing copies of the vm
    vm = vm.copy()

    output = vm.run([direction])
    assert len(output) == 1

    code = output[0]
    assert code in [WALL, OK, OXYGEN]

    return vm, code == OXYGEN, code == WALL


def solve_part2(program):
    # first bfs, from (0, 0) to explore the maze and find the oxygen source
    q = deque([(0, (0, 0), IntCodeVM(program))])
    ok = {(0, 0)}
    walls = set()
    oxygen = None
    while q:
        distance, position, vm = q.popleft()
        for direction in DIRECTIONS:
            next_pos = next_position(position, direction)
            if next_pos in ok or next_pos in walls:
                continue

            next_vm, is_oxygen, is_wall = move(vm, position, direction)

            if is_oxygen:
                oxygen = next_pos

            if is_wall:
                walls.add(next_pos)
            else:
                ok.add(next_pos)
                q.append((distance + 1, next_pos, next_vm))

    # second bfs, from the oxygen source, to find the point of the maze that is the
    # furthest from the source
    q = deque([(0, oxygen)])
    seen = {oxygen}
    max_distance = 0
    while q:
        distance, position = q.popleft()
        max_distance = distance
        for direction in DIRECTIONS:
            next_pos = next_position(position, direction)
            if next_pos in ok and next_pos not in seen:
                seen.add(next_pos)
                q.append((distance + 1, next_pos))

    return max_distance


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        program = list(map(int, s.split(",")))
        return solve_part2(program)
