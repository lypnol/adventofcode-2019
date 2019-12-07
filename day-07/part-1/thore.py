from collections import deque
from itertools import permutations

from tool.runners.python import SubmissionPy


class VM:
    def __init__(self, program):
        self.memory = list(program)
        self.pc = 0
        self.stdin = deque()
        self.stdout = deque()

    def step(self):
        instruction = self.memory[self.pc]
        opcode = instruction % 100

        if opcode == 1:  # ADD
            n_params = 3
            a_p, b_p, dest_p = self.get_params_pointers(instruction, n_params)
            self.memory[dest_p] = self.memory[a_p] + self.memory[b_p]
            self.pc += 1 + n_params
        elif opcode == 2:  # MUL
            n_params = 3
            a_p, b_p, dest_p = self.get_params_pointers(instruction, n_params)
            self.memory[dest_p] = self.memory[a_p] * self.memory[b_p]
            self.pc += 1 + n_params
        elif opcode == 3:  # IN
            n_params = 1
            dest_p, = self.get_params_pointers(instruction, n_params)
            value = self.stdin.popleft()
            self.memory[dest_p] = value
            self.pc += 1 + n_params
        elif opcode == 4:  # OUT
            n_params = 1
            a_p, = self.get_params_pointers(instruction, 1)
            value = self.memory[a_p]
            self.stdout.append(value)
            self.pc += 1 + n_params
        elif opcode == 5:  # JUMP-IF-TRUE
            n_params = 2
            cond_p, value_p = self.get_params_pointers(instruction, 2)
            if self.memory[cond_p] != 0:
                self.pc = self.memory[value_p]
            else:
                self.pc += 1 + n_params
        elif opcode == 6:  # JUMP-IF-FALSE
            n_params = 2
            cond_p, value_p = self.get_params_pointers(instruction, 2)
            if self.memory[cond_p] == 0:
                self.pc = self.memory[value_p]
            else:
                self.pc += 1 + n_params
        elif opcode == 7:  # LT
            n_params = 3
            a_p, b_p, dest_p = self.get_params_pointers(instruction, n_params)
            self.memory[dest_p] = int(self.memory[a_p] < self.memory[b_p])
            self.pc += 1 + n_params
        elif opcode == 8:  # EQ
            n_params = 3
            a_p, b_p, dest_p = self.get_params_pointers(instruction, n_params)
            self.memory[dest_p] = int(self.memory[a_p] == self.memory[b_p])
            self.pc += 1 + n_params
        elif opcode == 99:  # HALT
            return True
        else:
            raise f"Invalid opcode: {opcode}"

        return False

    def get_params_pointers(self, instruction, n_params):
        modes = [(instruction // 10 ** i) % 10 for i in range(2, 2 + n_params)]
        return [
            self.pc + 1 + i if modes[i] else self.memory[self.pc + 1 + i]
            for i in range(n_params)
        ]

    def run(self):
        finished = False
        while not finished:
            finished = self.step()

    def add_input(self, value):
        self.stdin.append(value)
        self.is_waiting_for_input = False

    def get_output(self):
        if len(self.stdout) == 0:
            return None
        return self.stdout.popleft()


def get_output(program, phase_setting_sequence):
    signal = 0

    for phase_setting in phase_setting_sequence:
        amplifier = VM(program)
        amplifier.add_input(phase_setting)
        amplifier.add_input(signal)
        amplifier.run()
        signal = amplifier.get_output()

    return signal


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        program = [int(i) for i in s.split(",")]
        N_AMPLIFIERS = 5

        return max(
            [get_output(program, seq) for seq in permutations(range(N_AMPLIFIERS))]
        )
