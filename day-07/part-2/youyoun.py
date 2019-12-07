from tool.runners.python import SubmissionPy
from typing import List
from itertools import permutations

MAX_PARAM_NUM = 3


class Amplifier:
    def __init__(self, phase):
        self.phase = phase
        self.input_signal = 0


class IntCode:
    def __init__(self, intcode: List, amplifier: Amplifier):
        self.intcode = intcode.copy()
        self.pos = 0
        self.opcode = 0
        self.amp = amplifier
        self.is_first_input = True
        self.outputs = []
        self.end = 0
        self.next = 0

    def set_input(self, inp):
        self.amp.input_signal = inp

    def move_pointer(self):
        if self.opcode in [1, 2, 7, 8]:
            self.pos += 4
        elif self.opcode in [5, 6]:
            self.pos += 3
        elif self.opcode in [3, 4]:
            self.pos += 2
        else:
            pass

    def run_instruction(self):
        instruction_code = self.intcode[self.pos]
        self.opcode, param_modes = parse_code(instruction_code)
        # 1002,4,3,4,33
        if self.opcode == 1:
            self.intcode[self.param(self.pos + 3, 0)] = self.intcode[self.param(self.pos + 1, param_modes[0])] \
                                                        + \
                                                        self.intcode[self.param(self.pos + 2, param_modes[1])]
        elif self.opcode == 2:
            self.intcode[self.param(self.pos + 3, 0)] = self.intcode[self.param(self.pos + 1, param_modes[0])] \
                                                        * \
                                                        self.intcode[self.param(self.pos + 2, param_modes[1])]
        elif self.opcode == 3:
            if self.is_first_input:
                self.intcode[self.param(self.pos + 1, param_modes[0])] = self.amp.phase
                self.is_first_input = False
            else:
                self.intcode[self.param(self.pos + 1, param_modes[0])] = self.amp.input_signal
        elif self.opcode == 4:
            self.outputs.append(self.intcode[self.param(self.pos + 1, param_modes[0])])
            self.next = 1
        elif self.opcode == 5:
            if self.intcode[self.param(self.pos + 1, param_modes[0])] != 0:
                self.pos = self.intcode[self.param(self.pos + 2, param_modes[1])]
                return  # dont run self.move_pointer
        elif self.opcode == 6:
            if self.intcode[self.param(self.pos + 1, param_modes[0])] == 0:
                self.pos = self.intcode[self.param(self.pos + 2, param_modes[1])]
                return
        elif self.opcode == 7:
            self.intcode[self.param(self.pos + 3, 0)] = int(self.intcode[self.param(self.pos + 1, param_modes[0])]
                                                            < self.intcode[self.param(self.pos + 2, param_modes[1])])
        elif self.opcode == 8:
            self.intcode[self.param(self.pos + 3, 0)] = int(self.intcode[self.param(self.pos + 1, param_modes[0])]
                                                            == self.intcode[self.param(self.pos + 2, param_modes[1])])
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
        outputs = []
        instructions = [int(x) for x in s.split(",")]
        for phases in permutations(range(5, 10)):
            out = 0
            amps = [IntCode(instructions, Amplifier(i)) for i in phases]
            while amps[-1].end == 0:
                for amplifier in amps:
                    amplifier.set_input(out)
                    while amplifier.end == 0 and amplifier.next == 0:
                        amplifier.run_instruction()
                    if amplifier.end == 0:
                        amplifier.next = 0
                    out = amplifier.outputs[-1]
            outputs.append(out)
        return max(outputs)
