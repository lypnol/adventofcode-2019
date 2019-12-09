from tool.runners.python import SubmissionPy
from typing import List

MAX_PARAM_NUM = 3


class InfList:
    def __init__(self, list_):
        self.list_ = list_

    def expand(self, value):
        self.list_.extend([0 for _ in range(value - len(self) + 1)])

    def __getitem__(self, item):
        if len(self) <= item:
            self.expand(item)
        return self.list_[item]

    def __setitem__(self, key, value):
        if len(self) <= key:
            self.expand(key)
        self.list_[key] = value

    def __len__(self):
        return len(self.list_)

    def __repr__(self):
        return repr(self.list_)


class Program:
    def __init__(self, intcode: List):
        self.intcode = InfList(intcode)
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
        # 1002,4,3,4,33
        if self.opcode == 1:
            self.intcode[self.param(self.pos + 3, param_modes[2])] = self.intcode[self.param(self.pos + 1, param_modes[0])] \
                                                        + \
                                                        self.intcode[self.param(self.pos + 2, param_modes[1])]
        elif self.opcode == 2:
            self.intcode[self.param(self.pos + 3, param_modes[2])] = self.intcode[self.param(self.pos + 1, param_modes[0])] \
                                                        * \
                                                        self.intcode[self.param(self.pos + 2, param_modes[1])]
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
            self.intcode[self.param(self.pos + 3, param_modes[2])] = int(self.intcode[self.param(self.pos + 1, param_modes[0])]
                                                            < self.intcode[self.param(self.pos + 2, param_modes[1])])
        elif self.opcode == 8:
            self.intcode[self.param(self.pos + 3, param_modes[2])] = int(self.intcode[self.param(self.pos + 1, param_modes[0])]
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
        prog = Program(instructions)
        while prog.end == 0:
            prog.run_instruction()
        return prog.outputs[-1]
