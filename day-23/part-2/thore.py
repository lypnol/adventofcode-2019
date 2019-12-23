from collections import defaultdict, deque

from tool.runners.python import SubmissionPy

N_COMPUTERS = 50


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        program = [int(c) for c in s.split(",")]
        computers = [VM(program) for _ in range(N_COMPUTERS)]

        # assign network addresses
        for i, computer in enumerate(computers):
            computer.add_input(i)

        nat = None
        nat_previously_sent = None
        while True:
            is_idle = True
            for computer in computers:

                if computer.is_waiting_for_input and len(computer.stdin) == 0:
                    computer.add_input(-1)
                else:
                    is_idle = False

                computer.run()

                while len(computer.stdout) > 0:
                    is_idle = False
                    address, x, y = computer.get_outputs(3)
                    if address == 255:
                        nat = x, y
                    else:
                        computers[address].add_input(x)
                        computers[address].add_input(y)

            if is_idle:
                x, y = nat
                computers[0].add_input(x)
                computers[0].add_input(y)
                if nat == nat_previously_sent:
                    return y
                nat_previously_sent = nat


#################### IntCode VM ####################


def list_to_dict(l):
    return dict(zip(range(len(l)), l))


class VM:
    def __init__(self, program, print_output=False):
        self.memory = defaultdict(float, list_to_dict(program))
        self.pc = 0
        self.relative_base = 0
        self.stdin = deque()
        self.stdout = deque()
        self.is_halted = False
        self.is_waiting_for_input = False
        self.print_output = print_output

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

    def get_outputs(self, n=3):
        if len(self.stdout) < n:
            return None
        return [self.stdout.popleft() for i in range(n)]

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
        pointers = [None] * n_params
        instruction //= 100
        for i in range(n_params):
            mode = instruction % 10
            instruction //= 10
            pointers[i] = self.get_param_pointer(mode, i + 1)
        return pointers

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
        if self.print_output:
            try:
                print(chr(value), end="")
            except ValueError:
                print("Unknown char:", value)
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

