from collections import defaultdict, deque

from tool.runners.python import SubmissionPy

EMPTY_ID = 0
WALL_ID = 1
BLOCK_ID = 2
PADDLE_ID = 3
BALL_ID = 4


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        program = [int(c) for c in s.split(",")]

        blocks = set()
        walls = set()
        paddle_pos = None
        ball_pos = None
        score = None

        vm = VM(program)
        vm.memory[0] = 2  # play for free

        it = 0
        while it == 0 or not vm.is_halted:
            vm.run()
            output = vm.get_outputs(3)
            while output is not None:
                if tuple(output[:2]) == (-1, 0):
                    score = output[2]
                elif output[2] == EMPTY_ID:
                    pos = tuple(output[:2])
                    if pos in blocks:
                        blocks.remove(pos)
                elif output[2] == WALL_ID:
                    walls.add(tuple(output[:2]))
                elif output[2] == BLOCK_ID:
                    blocks.add(tuple(output[:2]))
                elif output[2] == PADDLE_ID:
                    paddle_pos = tuple(output[:2])
                elif output[2] == BALL_ID:
                    ball_pos = tuple(output[:2])
                output = vm.get_outputs(3)
            joystick_dir = sign(ball_pos[0] - paddle_pos[0])
            vm.add_input(joystick_dir)
            it += 1
            print("Iteration", it)
            display_game(ball_pos, paddle_pos, blocks, walls, score)


def display_game(ball_pos, paddle_pos, blocks, walls, score):
    x_min = min(ball_pos, paddle_pos, *blocks, *walls, key=lambda p: p[0])[0]
    x_max = max(ball_pos, paddle_pos, *blocks, *walls, key=lambda p: p[0])[0]
    y_min = min(ball_pos, paddle_pos, *blocks, *walls, key=lambda p: p[1])[1]
    y_max = max(ball_pos, paddle_pos, *blocks, *walls, key=lambda p: p[1])[1]
    screen = [[" " for x in range(x_max + 1)] for y in range(y_max + 1)]
    screen[ball_pos[1]][ball_pos[0]] = "\u2B24"
    screen[paddle_pos[1]][paddle_pos[0]] = "="
    for block in blocks:
        screen[block[1]][block[0]] = "#"
    for wall in walls:
        screen[wall[1]][wall[0]] = "\u2588"
    print("Score:", score)
    print("\n".join(["".join(line) for line in screen]))


def get_blocks(program):
    print("######### Getting blocks #########")
    BLOCK_ID = 2
    vm = VM(program)
    vm.run()
    blocks = set()
    output = vm.get_outputs(3)
    while output is not None:
        if output[2] == BLOCK_ID:
            blocks.add(tuple(output[:2]))
        output = vm.get_outputs(3)
    print(blocks)
    return blocks


def sign(x):
    if x == 0:
        return 0
    return 1 if x > 0 else -1


def list_to_dict(l):
    return dict(zip(range(len(l)), l))


class VM:
    def __init__(self, program):
        self.memory = defaultdict(float, list_to_dict(program))
        self.pc = 0
        self.relative_base = 0
        self.stdin = deque()
        self.stdout = deque()
        self.is_halted = False
        self.is_waiting_for_input = False

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
        modes = [(instruction // 10 ** i) % 10 for i in range(2, 2 + n_params)]
        return [self.get_param_pointer(modes[i], i + 1) for i in range(n_params)]

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

