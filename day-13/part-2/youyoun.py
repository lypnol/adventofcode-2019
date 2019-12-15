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
        self.end = 0
        self.pointer_ref = 0

    def set_input(self, inp):
        self.input_value = inp
        self.outputs = []

    def clear_output(self):
        self.outputs = []

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


def parse_code(opcode):
    operation = opcode % 100
    all_modes = opcode // 100
    param_modes = [0 for _ in range(MAX_PARAM_NUM)]
    for i in range(MAX_PARAM_NUM):
        param_modes[i] = all_modes % 10
        all_modes = all_modes // 10
    return operation, param_modes


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        instructions = [int(x) for x in s.split(",")]
        instructions[0] = 2
        prog = Program(instructions)
        score = 0
        ball_pos = 0, 0
        paddle_pos = 0, 0
        while True:
            prog.run_instruction()
            if prog.end == 1:
                break
            if len(prog.outputs) == 3:
                x, y, c = prog.outputs
                if x == -1 and y == 0:
                    score = c
                else:
                    if c == 4:
                        ball_pos = x, y
                    elif c == 3:
                        paddle_pos = x, y
                prog.clear_output()
                if ball_pos[0] < paddle_pos[0]:
                    prog.set_input(-1)
                elif ball_pos[0] > paddle_pos[0]:
                    prog.set_input(1)
                else:
                    prog.set_input(0)
        return score
