from collections import defaultdict, deque
import re

from tool.runners.python import SubmissionPy

DETECTOR_ROOM = "Pressure-Sensitive Floor"
DO_NOT_TAKE_OBJECTS = [
    "molten lava",
    "infinite loop",
    "photons",
    "giant electromagnet",
    "escape pod",
]


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        program = [int(c) for c in s.split(",")]
        droid = VM(program)  # , print_io=True)  # , interactive=True)

        # Explore and take items
        adjacency_list, inventory, curr_pos = explore(droid)

        # Go to security checkpoint
        path_to_detector = bfs(adjacency_list, curr_pos, DETECTOR_ROOM)
        follow_path(droid, path_to_detector[:-1])

        # Bruteforce pressure-sensitive floor
        return bruteforce_detector(droid, inventory, path_to_detector[-1])


def bruteforce_detector(droid, inventory, door):
    def power_set(objects):
        droid.add_input_ascii(door)
        droid.run()
        password = parse_password(droid.get_output_ascii())
        if password is not None:
            return password

        if len(objects) > 0:
            droid.add_input_ascii("take " + objects[0])
            droid.run()
            droid.get_output_ascii()
            password = power_set(objects[1:])
            if password is not None:
                return password
            else:
                droid.add_input_ascii("drop " + objects[0])
                droid.run()
                droid.get_output_ascii()

        if len(objects) > 0:
            password = power_set(objects[1:])
            if password is not None:
                return password

        return None

    return power_set(list(inventory))


def parse_password(output):
    m = re.search("You should be able to get in by typing (\d+)", output)
    if m:
        return m.group(1)
    else:
        return None


def follow_path(droid, path):
    for door in path:
        droid.add_input_ascii(door)
        droid.run()
        droid.get_output_ascii()


def bfs(adjacency_list, frm, to):
    q = deque([(frm, None)])
    seen = {}
    while len(q) > 0:
        n, prev = q.popleft()

        if n in seen:
            continue
        seen[n] = prev

        if n == to:
            break

        for door, neighbour in adjacency_list[n]:
            q.append((neighbour, (n, door)))

    path = []
    pos = to
    while pos != frm:
        pos, door = seen[pos]
        path.append(door)

    return list(reversed(path))


def explore(droid):
    droid.run()
    adjacency_list = {}
    inventory = set()

    def explore_backtracking():
        name, objects, doors = parse_output(droid.get_output_ascii())
        if name in adjacency_list:
            return name

        for obj in objects:
            if obj in DO_NOT_TAKE_OBJECTS:
                continue
            inventory.add(obj)
            droid.add_input_ascii("take " + obj)
            droid.run()
            droid.get_output_ascii()
        adjacency_list[name] = []

        for d in doors:
            droid.add_input_ascii(d)
            droid.run()
            new_name = explore_backtracking()
            adjacency_list[name].append((d, new_name))
            if name != new_name:
                droid.add_input_ascii(opposite_direction(d))
                droid.run()
                droid.get_output_ascii()

        return name

    curr_pos = explore_backtracking()
    return adjacency_list, inventory, curr_pos


def opposite_direction(direction):
    if direction == "north":
        return "south"
    elif direction == "south":
        return "north"
    elif direction == "west":
        return "east"
    elif direction == "east":
        return "west"
    else:
        raise ValueError(f"Unknown direction: {direction}")


def parse_output(output):
    name_match = re.search("== (.*) ==", output)
    name = name_match.group(1) if name_match else ""

    objects_match = re.search("Items here:\n((- .+\n)+)\n", output)
    if objects_match:
        objects_str = objects_match.group(1)
        objects = [m.group(1) for m in re.finditer("- (.*)", objects_str)]
    else:
        objects = []

    doors_match = re.search("Doors here lead:\n((- .+\n)+)\n", output)
    if doors_match:
        doors_str = doors_match.group(0)
        doors = [m.group(1) for m in re.finditer("- (.*)", doors_str)]
    else:
        doors = []

    return name, objects, doors


#################### IntCode VM ####################


def list_to_dict(l):
    return dict(zip(range(len(l)), l))


class VM:
    def __init__(self, program, print_io=False, interactive_input=False):
        self.memory = defaultdict(float, list_to_dict(program))
        self.pc = 0
        self.relative_base = 0
        self.stdin = deque()
        self.stdout = deque()
        self.is_halted = False
        self.is_waiting_for_input = False
        self.print_io = print_io
        self.interactive_input = interactive_input

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

    def add_input_ascii(self, s, end="\n"):
        for c in s:
            self.add_input(ord(c))
        self.add_input(ord(end))

    def get_output(self):
        if len(self.stdout) == 0:
            return None
        return self.stdout.popleft()

    def get_outputs(self, n=3):
        if len(self.stdout) < n:
            return None
        return [self.stdout.popleft() for i in range(n)]

    def get_output_ascii(self):
        s = "".join(chr(o) for o in self.stdout)
        self.stdout = deque()
        return s

    def run_ascii_command(self, command):
        self.add_input_ascii(command)
        self.run()
        return self.get_output_ascii()

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
            if self.interactive_input:
                inp = input() + "\n"
                for c in inp:
                    self.stdin.append(ord(c))
            else:
                self.is_waiting_for_input = True
                return None
        value = self.stdin.popleft()
        if self.print_io:
            try:
                print(chr(value), end="")
            except ValueError:
                print("Unknown char:", value)
        self.memory[dest_p] = value
        return self.pc + 2

    def op_output(self, a_p):
        value = self.memory[a_p]
        self.stdout.append(value)
        if self.print_io:
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

