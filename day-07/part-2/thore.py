from collections import deque
from itertools import permutations

from tool.runners.python import SubmissionPy


class VM:
    def __init__(self, program):
        self.memory = list(program)
        self.pc = 0
        self.stdin = deque()
        self.stdout = deque()
        self.is_halted = False
        self.is_waiting_for_input = False

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
            if len(self.stdin) == 0:
                self.is_waiting_for_input = True
                return
            self.is_waiting_for_input = False
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
            self.is_halted = True
            return
        else:
            raise f"Invalid opcode: {opcode}"

        return

    def get_params_pointers(self, instruction, n_params):
        modes = [(instruction // 10 ** i) % 10 for i in range(2, 2 + n_params)]
        return [
            self.pc + 1 + i if modes[i] else self.memory[self.pc + 1 + i]
            for i in range(n_params)
        ]

    def run(self):
        while not self.is_halted and not self.is_waiting_for_input:
            self.step()

    def add_input(self, value):
        self.stdin.append(value)
        self.is_waiting_for_input = False

    def get_output(self):
        if len(self.stdout) == 0:
            return None
        return self.stdout.popleft()


def get_output(program, phase_setting_sequence):
    amplifiers = [VM(program) for _ in phase_setting_sequence]
    for amplifier, phase_setting in zip(amplifiers, phase_setting_sequence):
        amplifier.stdin.append(phase_setting)

    signal = 0
    i = 0
    it, max_it = 0, 1e6
    while it < max_it:
        amplifier = amplifiers[i]
        amplifier.add_input(signal)
        amplifier.run()
        signal = amplifier.get_output()

        if i == len(amplifiers) - 1 and amplifier.is_halted:
            break

        i = (i + 1) % len(amplifiers)
        it += 1

    if it == max_it:
        raise "Error: max number of iterations reached"

    return signal


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        program = [int(i) for i in s.split(",")]
        phase_settings = range(5, 10)

        return max([get_output(program, seq) for seq in permutations(phase_settings)])
