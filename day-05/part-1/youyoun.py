from tool.runners.python import SubmissionPy

MAX_PARAM_NUM = 3


class IntCode:
    def __init__(self, intcode):
        self.intcode = intcode
        self.pos = 0
        self.opcode = 0
        self.input_value = 1
        self.outputs = []
        self.end = 0

    def next_instruction(self):
        if self.opcode in [1, 2]:
            self.pos += 4
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
            self.intcode[self.param(self.pos + 1, param_modes[0])] = self.input_value
        elif self.opcode == 4:
            self.outputs.append(self.intcode[self.param(self.pos + 1, param_modes[0])])
        elif self.opcode == 99:
            self.end = 1
        else:
            raise ValueError("Invalid op code")
        self.next_instruction()
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
        intcode = IntCode([int(x) for x in s.split(",")])
        while intcode.end == 0:
            intcode.run_instruction()
        return intcode.outputs[-1]
