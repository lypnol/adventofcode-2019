from collections import defaultdict, deque
from enum import IntEnum

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        program = [int(i) for i in s.split(",")]
        environment = defaultdict(int)
        environment[(0, 0)] = 1
        robot = Robot(program, environment)

        while not robot.is_halted:
            robot.step()

        # print(pprint(environment, pretty=True))
        return pprint(environment)


def pprint(environment, pretty=False):
    if pretty:
        c1, c0 = "#", "."
    else:
        c1, c0 = "1", "0"

    x_max = max([pos[0] for pos in environment.keys()])
    x_min = min([pos[0] for pos in environment.keys()])
    y_max = max([pos[1] for pos in environment.keys()])
    y_min = min([pos[1] for pos in environment.keys()])

    return "\n".join(
        [
            "".join(
                [
                    c1 if environment[(x, y)] == 1 else c0
                    for x in range(x_min + 1, x_max - 1)
                ]
            )
            for y in range(y_max, y_min - 1, -1)
        ]
    )


class Robot:
    def __init__(self, program, environment):
        self.pos = (0, 0)
        self.direction = Direction.UP
        self.brain = VM(program)
        self.environment = environment
        self.painted_panels = set()

    @property
    def is_halted(self):
        return self.brain.is_halted

    def step(self):
        self.brain.add_input(self.environment[self.pos])
        self.brain.run()

        if self.brain.is_halted:
            return

        color = self.brain.get_output()
        next_direction_angle = self.brain.get_output()

        self.environment[self.pos] = color
        self.painted_panels.add(self.pos)

        if next_direction_angle == 0:
            self.direction = (self.direction - 1) % 4
        else:
            self.direction = (self.direction + 1) % 4

        self.move_forward()

    def move_forward(self):
        x, y = self.pos
        if self.direction == Direction.UP:
            self.pos = (x, y + 1)
        elif self.direction == Direction.RIGHT:
            self.pos = (x + 1, y)
        elif self.direction == Direction.DOWN:
            self.pos = (x, y - 1)
        elif self.direction == Direction.LEFT:
            self.pos = (x - 1, y)


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def list_to_dict(l):
    return dict(zip(range(len(l)), l))


class VM:
    def __init__(self, program):
        self.memory = defaultdict(float, list_to_dict(program))
        self.pc = 0
        self.relative_base = 0
        self.stdin = deque()
        self.stdout = deque()
        self.is_halted = False
        self.is_waiting_for_input = False

        self.opcodes = {
            1: (self.op_add, 3),
            2: (self.op_mul, 3),
            3: (self.op_input, 1),
            4: (self.op_output, 1),
            5: (self.op_jump_if_true, 2),
            6: (self.op_jump_if_false, 2),
            7: (self.op_lt, 3),
            8: (self.op_eq, 3),
            9: (self.op_rel_base, 1),
            99: (self.op_halt, 0),
        }

    def add_input(self, value):
        self.stdin.append(value)
        self.is_waiting_for_input = False

    def get_output(self):
        if len(self.stdout) == 0:
            return None
        return self.stdout.popleft()

    def run(self):
        while not self.is_halted and not self.is_waiting_for_input:
            self.step()

    def step(self):
        instruction = self.memory[self.pc]
        opcode = instruction % 100

        if opcode not in self.opcodes:
            raise f"Invalid opcode: {opcode}"

        op_func, n_params = self.opcodes[opcode]
        params = self.get_params_pointers(instruction, n_params)
        pc = op_func(*params)
        if pc is not None:
            self.pc = pc

        return

    def get_params_pointers(self, instruction, n_params):
        modes = [(instruction // 10 ** i) % 10 for i in range(2, 2 + n_params)]
        return [self.get_param_pointer(modes[i], i + 1) for i in range(n_params)]

    def get_param_pointer(self, mode, pos):
        if mode == 0:
            return self.memory[self.pc + pos]
        elif mode == 1:
            return self.pc + pos
        elif mode == 2:
            return self.relative_base + self.memory[self.pc + pos]
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def op_add(self, a_p, b_p, dest_p):
        self.memory[dest_p] = self.memory[a_p] + self.memory[b_p]
        return self.pc + 4

    def op_mul(self, a_p, b_p, dest_p):
        self.memory[dest_p] = self.memory[a_p] * self.memory[b_p]
        return self.pc + 4

    def op_input(self, dest_p):
        if len(self.stdin) == 0:
            self.is_waiting_for_input = True
            return None
        value = self.stdin.popleft()
        self.memory[dest_p] = value
        return self.pc + 2

    def op_output(self, a_p):
        value = self.memory[a_p]
        self.stdout.append(value)
        return self.pc + 2

    def op_jump_if_true(self, cond_p, value_p):
        if self.memory[cond_p] != 0:
            return self.memory[value_p]
        else:
            return self.pc + 3

    def op_jump_if_false(self, cond_p, value_p):
        if self.memory[cond_p] == 0:
            return self.memory[value_p]
        else:
            return self.pc + 3

    def op_lt(self, a_p, b_p, dest_p):
        self.memory[dest_p] = int(self.memory[a_p] < self.memory[b_p])
        return self.pc + 4

    def op_eq(self, a_p, b_p, dest_p):
        self.memory[dest_p] = int(self.memory[a_p] == self.memory[b_p])
        return self.pc + 4

    def op_rel_base(self, val_p):
        self.relative_base += self.memory[val_p]
        return self.pc + 2

    def op_halt(self):
        self.is_halted = True
        return None
