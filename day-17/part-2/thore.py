from collections import defaultdict, deque

from tool.runners.python import SubmissionPy

SCAFFOLD = "#"
ROBOT = "^>v<"
DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
SCAFFOLD_CHARS = SCAFFOLD + ROBOT


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        program = [int(c) for c in s.split(",")]

        robot = VM(program)  # , print_output=True)
        robot.memory[0] = 2  # Wake up

        robot.run()
        world = "".join(chr(d) for d in robot.stdout).rstrip().splitlines()[:-2]

        instructions = generate_instructions(world)
        main, functions = compress_instructions(instructions)

        main_map = ["A", "B", "C"]
        main_str = ",".join([main_map[f] for f in main])
        functions_str = "\n".join(",".join(f) for f in functions)
        logic = "\n".join([main_str, functions_str, "n"])

        # print(f"Uncompressed:\n{instructions}\n")
        # print(f"Compressed:\n{logic}")

        for line in logic.splitlines():
            for c in line:
                robot.add_input(ord(c))
            robot.add_input(ord("\n"))

        robot.run()

        return robot.stdout[-1]


def generate_instructions(world):
    pos = find_robot(world)
    direction = ROBOT.find(world[pos[0]][pos[1]])
    assert direction != -1

    instructions = []
    dead_end = False
    forward_count = 0
    while not dead_end:
        next_pos = get_next_pos(pos, direction)
        if is_scaffold(world, next_pos):  # Go forward
            pos = next_pos
            forward_count += 1
        else:
            if forward_count > 0:  # Flush forward moves
                instructions.append(str(forward_count))
                forward_count = 0
            next_pos_r = get_next_pos(pos, (direction + 1) % len(ROBOT))
            next_pos_l = get_next_pos(pos, (direction - 1) % len(ROBOT))
            if is_scaffold(world, next_pos_r):  # Turn right
                direction = (direction + 1) % len(ROBOT)
                instructions.append("R")
            elif is_scaffold(world, next_pos_l):  # Turn left
                direction = (direction - 1) % len(ROBOT)
                instructions.append("L")
            else:
                dead_end = True  # End

    return ",".join(instructions)


def get_next_pos(pos, direction):
    delta = DELTAS[direction]
    return (pos[0] + delta[0], pos[1] + delta[1])


def is_scaffold(world, pos):
    try:
        return world[pos[0]][pos[1]] in SCAFFOLD_CHARS
    except IndexError:
        return False


def find_robot(world):
    width = len(world[0]) + 1
    idx = sum("\n".join(world).find(r) for r in ROBOT) + len(ROBOT) - 1
    return (idx // width, idx % width)


def compress_instructions(instructions, max_dict_size=3, max_chars=10, min_code_size=4):
    instructions = instructions.split(",")
    compressed = []
    codes = []

    def compress_backtracking(frm):
        if frm == len(instructions):
            return True

        # Check if prefix match existing code
        for i, code in enumerate(codes):
            if (
                len(code) > 0
                and len(compressed) < max_chars
                and instructions[frm : frm + len(code)] == code
            ):
                compressed.append(i)
                appended_code = False

                if compress_backtracking(frm + len(code)):
                    return True
                else:
                    compressed.pop()

        # Try to extend last code
        if (
            len(codes) > 0
            and len(codes[-1]) < max_chars
            and codes[-1] == instructions[frm - len(codes[-1]) : frm]
        ):
            codes[-1].append(instructions[frm])
            if compress_backtracking(frm + 1):
                return True
            else:
                codes[-1].pop()

        # Try to create a new code
        if (
            len(codes) < max_dict_size
            and (len(codes) == 0 or len(codes[-1]) >= min_code_size)
            and len(compressed) < max_chars
        ):
            codes.append([instructions[frm]])
            compressed.append(len(codes) - 1)
            if compress_backtracking(frm + 1):
                return True
            else:
                codes.pop()
                compressed.pop()
        return False

    compress_backtracking(0)
    return compressed, codes


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
            print(chr(value), end="")
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

