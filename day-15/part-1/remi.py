from tool.runners.python import SubmissionPy

from itertools import permutations
from random import randint

palette = {0: " ", 1: "#", 2: "x", 3: "_", 4: "o"}


class RemiSubmission(SubmissionPy):
    def run(self, s):
        p = [int(n) for n in s.split(",")]
        droid = IntCode(p)

        self.maze = {(0, 0): "."}
        self.coor = (0, 0)
        self.path = [(0, 0)]
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        direction = 0

        while True:
            droid.p_input.append(direction + 1)
            droid.execute()
            code = droid.p_output.pop()
            if code == 0:
                self.maze[
                    (
                        self.coor[0] + self.directions[direction][0],
                        self.coor[1] + self.directions[direction][1],
                    )
                ] = "#"
                direction = self.choose_new_direction()
            elif code == 1:
                self.maze[
                    (
                        self.coor[0] + self.directions[direction][0],
                        self.coor[1] + self.directions[direction][1],
                    )
                ] = "."
                self.coor = (
                    self.coor[0] + self.directions[direction][0],
                    self.coor[1] + self.directions[direction][1],
                )
                self.path.append(self.coor)
            elif code == 2:
                self.maze[
                    (
                        self.coor[0] + self.directions[direction][0],
                        self.coor[1] + self.directions[direction][1],
                    )
                ] = "."
                self.coor = (
                    self.coor[0] + self.directions[direction][0],
                    self.coor[1] + self.directions[direction][1],
                )
                self.path.append(self.coor)
                break

        self.display_maze()

        while self.minimize_path():
            pass

        return len(self.path) - 1

    def minimize_path(self):
        min_path = []
        i = 0
        changed = False
        while i < len(self.path):
            if i < len(self.path) - 2 and self.path[i] == self.path[i + 2]:
                changed = True
                min_path.append(self.path[i])
                i += 3
            else:
                min_path.append(self.path[i])
                i += 1
        self.path = min_path

        return changed

    def choose_new_direction(self):
        neighbours = []
        for direction in range(len(self.directions)):
            coor = (
                self.coor[0] + self.directions[direction][0],
                self.coor[1] + self.directions[direction][1],
            )
            tile = self.maze.get(coor, "?")
            if tile == "#":
                neighbours.append(0)
            elif tile == ".":
                neighbours.append(1)
            elif tile == "?":
                neighbours.append(2)

        return max(
            (i for i in range(len(self.directions))), key=lambda i: neighbours[i]
        )

    def display_maze(self):
        maxx = max(x for (x, y) in self.maze.keys())
        minx = min(x for (x, y) in self.maze.keys())
        maxy = max(y for (x, y) in self.maze.keys())
        miny = min(y for (x, y) in self.maze.keys())

        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                print(self.maze.get((x, y), "#"), end="")
            print("")
        print("")


class IntCode:
    def __init__(self, p):
        self.p = [0] * (10 * len(p))
        for i, b in enumerate(p):
            self.p[i] = b

        self.pc = 0
        self.p_input = []
        self.p_output = []
        self.exited = False
        self.relative_base = 0

    def get_param_p(self, index):
        param = self.p[self.pc + index + 1]
        opcode = self.p[self.pc]
        modes = opcode // 100
        for _ in range(index):
            modes //= 10
        mode = modes % 10

        if mode == 0:
            return param
        elif mode == 1:
            return None
        elif mode == 2:
            return param + self.relative_base

    def get_param(self, index):
        d = self.get_param_p(index)
        if d is not None:
            return self.p[d]
        else:
            # for immediate mode
            return self.p[self.pc + index + 1]

    def execute(self):
        if self.exited:
            return

        while True:
            opcode = self.p[self.pc]
            if opcode % 100 == 1:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                self.p[c] = a + b
                self.pc += 4

            elif opcode % 100 == 2:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                self.p[c] = a * b
                self.pc += 4

            elif opcode % 100 == 3:
                try:
                    a = self.get_param_p(0)
                    self.p[a] = self.p_input[0]
                    self.p_input = self.p_input[1:]
                except:
                    return
                self.pc += 2

            elif opcode % 100 == 4:
                self.p_output.append(self.get_param(0))
                self.pc += 2

            elif opcode % 100 == 5:
                a = self.get_param(0)
                b = self.get_param(1)
                if a != 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 6:
                a = self.get_param(0)
                b = self.get_param(1)
                if a == 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 7:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                if a < b:
                    self.p[c] = 1
                else:
                    self.p[c] = 0
                self.pc += 4

            elif opcode % 100 == 8:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                if a == b:
                    self.p[c] = 1
                else:
                    self.p[c] = 0
                self.pc += 4

            elif opcode % 100 == 9:
                a = self.get_param(0)
                self.relative_base += a
                self.pc += 2

            elif opcode % 100 == 99:
                self.exited = True
                break

        return
