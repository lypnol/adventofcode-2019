from collections import defaultdict, deque
import heapq
from random import choice
from enum import IntEnum
from os import system

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        program = [int(c) for c in s.split(",")]
        droid = Droid(program)  # , verbose=True)
        droid.explore_map()
        return oxygen_filling_time(droid.world, droid.oxygen_pos)  # , verbose=True)


def oxygen_filling_time(world, oxygen_src, verbose=False):
    directions = [d.value for d in Direction]
    frontier = deque([(oxygen_src, 0)])
    visited = set()
    farthest_point = 0
    while len(frontier) > 0:
        pos, dist = frontier.popleft()
        if pos in visited:
            continue
        if dist > farthest_point:
            farthest_point = dist
        for d in directions:
            new_pos = get_new_pos(pos, d)
            if world[new_pos] == Tile.WALL:
                continue
            frontier.append((new_pos, dist + 1))

        visited.add(pos)
        if verbose:
            world[pos] = Tile.OXYGEN
            system("clear")
            print(pprint_world(world, pos))

    return farthest_point


class Tile(IntEnum):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2
    VISITED = 10


class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


def reverse_dir(direction):
    return direction + 1 if direction % 2 == 1 else direction - 1


def euclidean_dist(pos1, pos2):
    return sum([abs(x1 - x2) for x1, x2 in zip(pos1, pos2)])


class Droid:
    def __init__(self, program, verbose=False):
        self.cpu = VM(program)
        self.verbose = verbose
        self.pos = (0, 0)
        self.world = {self.pos: 0}
        self.oxygen_pos = None
        self.directions = [d.value for d in Direction]

    def get_tile(self):
        return self.world[self.pos]

    def find_oxygen(self):
        if self.oxygen_pos is None:
            self.explore_map()
        return self._a_star(self.oxygen_pos)

    def _a_star(self, target):
        if self.verbose:
            world_astar = self.world.copy()

        visited = set()
        queue = []
        heapq.heappush(queue, (euclidean_dist(self.pos, target), self.pos, 0))
        while len(queue) > 0:
            dist_remaining, pos, dist_to = heapq.heappop(queue)

            if self.verbose:
                world_astar[pos] = Tile.VISITED
                system("clear")
                print(pprint_world(world_astar, pos))

            if pos == self.oxygen_pos:
                return dist_to

            for d in self.directions:
                new_pos = get_new_pos(pos, d)
                if self.world[new_pos] == Tile.WALL or new_pos in visited:
                    continue

                heapq.heappush(
                    queue, (euclidean_dist(new_pos, target), new_pos, 1 + dist_to)
                )

            visited.add(pos)

        return float("inf")

    def explore_map(self):
        if self.get_tile() == Tile.OXYGEN:
            self.oxygen_pos = self.pos

        new_dirs = self._get_new_directions()
        while len(new_dirs) > 0:
            d = choice(new_dirs)
            moved = self.step(d)
            self.explore_map()
            if moved:
                self.step(reverse_dir(d))
            new_dirs = self._get_new_directions()

    def _get_new_directions(self):
        return [
            d for d in self.directions if get_new_pos(self.pos, d) not in self.world
        ]

    def step(self, direction):
        self.cpu.add_input(direction)
        self.cpu.run()
        output = self.cpu.get_output()
        self._update(direction, output)

        if self.verbose:
            system("clear")
            print(pprint_world(self.world, self.pos))

        return output != Tile.WALL

    def _update(self, direction, output):
        new_pos = get_new_pos(self.pos, direction)
        self.world[new_pos] = output
        if output != Tile.WALL:
            self.pos = new_pos


def get_new_pos(pos, direction):
    if pos is None:
        pos = self.pos
    if direction == Direction.NORTH:
        new_pos = (pos[0], pos[1] + 1)
    elif direction == Direction.SOUTH:
        new_pos = (pos[0], pos[1] - 1)
    elif direction == Direction.WEST:
        new_pos = (pos[0] - 1, pos[1])
    elif direction == Direction.EAST:
        new_pos = (pos[0] + 1, pos[1])
    else:
        raise ValueError(f"Invalid direction: {direction}")
    return new_pos


def pprint_world(world, pos):
    chars = {
        Tile.EMPTY: "\u00b7",
        Tile.WALL: "\u2588",
        Tile.OXYGEN: "O",
        Tile.VISITED: "x",
    }
    xmin, xmax = min([p[0] for p in world]), max([p[0] for p in world])
    ymin, ymax = min([p[1] for p in world]), max([p[1] for p in world])

    return "\n".join(
        [
            "".join(
                [
                    "#"
                    if (x, y) == pos
                    else (chars[world[(x, y)]] if (x, y) in world else " ")
                    for x in range(xmin, xmax + 1)
                ]
            )
            for y in range(ymax, ymin - 1, -1)
        ]
    )


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

