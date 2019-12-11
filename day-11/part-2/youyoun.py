from tool.runners.python import SubmissionPy
from typing import List
from collections import defaultdict

MAX_PARAM_NUM = 3


class Program:
    def __init__(self, intcode: List):
        self.intcode = defaultdict(int)
        for i in range(len(intcode)):
            self.intcode[i] = intcode[i]
        self.pos = 0
        self.opcode = 0
        self.input_value = 1
        self.outputs = []
        self.next = 0
        self.end = 0
        self.pointer_ref = 0

    def set_input(self, inp):
        self.input_value = inp
        self.next = 0

    def move_pointer(self):
        if self.opcode in [1, 2, 7, 8]:
            self.pos += 4
        elif self.opcode in [5, 6]:
            self.pos += 3
        elif self.opcode in [3, 4, 9]:
            self.pos += 2
        else:
            pass

    def run_instruction(self):
        instruction_code = self.intcode[self.pos]
        self.opcode, param_modes = parse_code(instruction_code)
        # 1002,4,3,4,33
        if self.opcode == 1:
            self.intcode[self.param(self.pos + 3, param_modes[2])] = self.intcode[
                                                                         self.param(self.pos + 1, param_modes[0])] \
                                                                     + \
                                                                     self.intcode[
                                                                         self.param(self.pos + 2, param_modes[1])]
        elif self.opcode == 2:
            self.intcode[self.param(self.pos + 3, param_modes[2])] = self.intcode[
                                                                         self.param(self.pos + 1, param_modes[0])] \
                                                                     * \
                                                                     self.intcode[
                                                                         self.param(self.pos + 2, param_modes[1])]
        elif self.opcode == 3:
            self.intcode[self.param(self.pos + 1, param_modes[0])] = self.input_value
        elif self.opcode == 4:
            self.outputs.append(self.intcode[self.param(self.pos + 1, param_modes[0])])
            self.next += 1
        elif self.opcode == 5:
            if self.intcode[self.param(self.pos + 1, param_modes[0])] != 0:
                self.pos = self.intcode[self.param(self.pos + 2, param_modes[1])]
                return  # dont run self.move_pointer
        elif self.opcode == 6:
            if self.intcode[self.param(self.pos + 1, param_modes[0])] == 0:
                self.pos = self.intcode[self.param(self.pos + 2, param_modes[1])]
                return
        elif self.opcode == 7:
            self.intcode[self.param(self.pos + 3, param_modes[2])] = int(
                self.intcode[self.param(self.pos + 1, param_modes[0])]
                < self.intcode[self.param(self.pos + 2, param_modes[1])])
        elif self.opcode == 8:
            self.intcode[self.param(self.pos + 3, param_modes[2])] = int(
                self.intcode[self.param(self.pos + 1, param_modes[0])]
                == self.intcode[self.param(self.pos + 2, param_modes[1])])
        elif self.opcode == 9:
            self.pointer_ref += self.intcode[self.param(self.pos + 1, param_modes[0])]
        elif self.opcode == 99:
            self.end = 1
            self.next = 2
        else:
            raise ValueError("Invalid op code")
        self.move_pointer()
        return

    def param(self, pos, mode):
        if mode == 0:
            return self.intcode[pos]
        elif mode == 1:
            return pos
        elif mode == 2:
            return self.pointer_ref + self.intcode[pos]
        else:
            raise ValueError("Invalid parameter mode")


def parse_code(opcode):
    operation = opcode % 100
    all_modes = opcode // 100
    param_modes = [0 for _ in range(MAX_PARAM_NUM)]
    for i in range(MAX_PARAM_NUM):
        param_modes[i] = all_modes % 10
        all_modes = all_modes // 10
    return operation, param_modes


# 0 down, 1 left, 2 up, 3 right
MVTS = {
    0: (0, 1),
    1: (-1, 0),
    2: (0, -1),
    3: (1, 0),
}


class Robot:
    def __init__(self):
        self.x = -1
        self.y = 0
        self.dir = 2

    def get_position(self):
        return self.x, self.y

    def move(self, direction):
        if direction == 0:
            self.dir = (self.dir - 1) % 4
        else:
            self.dir = (self.dir + 1) % 4
        mvt = MVTS[self.dir]
        self.x += mvt[0]
        self.y += mvt[1]


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        arr = []
        pannels = defaultdict(int)
        robot = Robot()
        instructions = [int(x) for x in s.split(",")]
        prog = Program(instructions)
        prog.set_input(1)
        while prog.end == 0:
            while prog.next < 2:
                prog.run_instruction()
            pannels[robot.get_position()] = prog.outputs[-2]
            robot.move(prog.outputs[-1])
            prog.set_input(pannels[robot.get_position()])
        img = [str(pannels[(i,j)]) for j in range(6) for i in range(40)]
        return "".join(img)
