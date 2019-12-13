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
        vm = VM(program)
        vm.memory[0] = 2  # play for free

        return play(vm)


def play(vm, verbose=False):
    screen = defaultdict(int)
    ball_pos, paddle_pos = None, None
    score = 0
    it = 0
    while not vm.is_halted:
        vm.run()

        # process outputs
        while len(vm.stdout) >= 3:
            output = vm.get_outputs(3)
            pos, tile_id = tuple(output[:2]), output[2]
            if pos == (-1, 0):
                score = tile_id
            else:
                screen[pos] = tile_id

                if tile_id == BALL_ID:
                    ball_pos = pos
                elif tile_id == PADDLE_ID:
                    paddle_pos = pos

        # choose joystick direction
        joystick_dir = sign(ball_pos[0] - paddle_pos[0])
        vm.add_input(joystick_dir)

        it += 1

        if verbose:
            print("\nIteration", it)
            print("Score:", score)
            display(screen)
    return score


def display(screen):
    x_max = max([pos[0] for pos in screen.keys()])
    y_max = max([pos[1] for pos in screen.keys()])

    tile_to_chr = {
        EMPTY_ID: " ",
        WALL_ID: "\u2588",
        BLOCK_ID: "#",
        PADDLE_ID: "=",
        BALL_ID: "\u2B24",
    }

    print(
        "\n".join(
            [
                "".join([tile_to_chr[screen[(x, y)]] for x in range(x_max + 1)])
                for y in range(y_max + 1)
            ]
        )
    )


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

