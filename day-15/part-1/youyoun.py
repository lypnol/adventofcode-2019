from tool.runners.python import SubmissionPy
from typing import List
from collections import defaultdict
import numpy as np

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
        self.end = 0
        self.pointer_ref = 0

    def set_input(self, inp):
        self.input_value = inp

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

    def clear_output(self):
        self.outputs = []


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

DIR_INPUT = {
    0: 2,
    1: 3,
    2: 1,
    3: 4,
}

DIR_CHAR = {
    0: "v",
    1: "<",
    2: "^",
    3: ">",
}


class Robot:
    def __init__(self):
        self.x = 21
        self.y = 21
        self.dir = 0
        self.map = defaultdict(set)

    @property
    def input(self):
        return DIR_INPUT[self.dir]

    def get_position(self):
        return self.x, self.y

    def move(self, output):
        mvt = MVTS[self.dir]
        if output == 0:
            self.dir = (self.dir + 1) % 4
        else:
            new_pos = self.x + mvt[0], self.y + mvt[1]
            self.map[(self.x, self.y)].add(new_pos)
            self.map[new_pos].add((self.x, self.y))
            self.x, self.y = new_pos
            self.dir = (self.dir - 1) % 4


def add_pos(pos1, pos2):
    return pos1[0] + pos2[0], pos1[1] + pos2[1]


def shortest_route(map, start, end):
    next_pos = [e for e in map[start]][0] if len(map[start]) > 0 else None
    if next_pos is None:
        return 0
    q = {(1, next_pos, start)}
    steps_set = set()
    while len(q) != 0:
        steps, pos, prev_pos = q.pop()
        for n in map[pos]:
            if prev_pos == n:
                continue
            if n == end:
                steps_set.add(steps + 1)
            q.add((steps + 1, n, pos))
    return min(steps_set) if len(steps_set) > 0 else 0


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        robot = Robot()
        init_pos = robot.get_position()
        passed = 0
        oxyg = None
        instructions = [int(x) for x in s.split(",")]
        prog = Program(instructions)
        prog.set_input(robot.input)
        while prog.end == 0:
            prog.run_instruction()
            if len(prog.outputs) == 1:
                output = prog.outputs[0]
                robot.move(output)
                prog.clear_output()
                prog.set_input(robot.input)
                if output == 2:
                    oxyg = robot.get_position()
                if robot.get_position() == init_pos:
                    passed += 1
                if passed == 2:
                    break
        return shortest_route(robot.map, init_pos, oxyg)
