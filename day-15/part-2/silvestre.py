import sys
import collections

from tool.runners.python import SubmissionPy

DIRECTIONS = {
    1: (0, 1),  # North
    2: (0, -1), # South
    3: (-1, 0), # West
    4: (1, 0),  # East
}

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        # intcode stuff
        code = [int(i) for i in s.strip().split(",")]
        input_l = [0]
        computer = compute(code, input_l)

        # actual problem stuff
        pos = (0, 0)
        pos_oxygen = None
        grid = {pos: 1}

        to_explore = collections.deque([pos_add(pos, d) for d in DIRECTIONS.values()])

        seen = {pos}
        seen.update(to_explore)
        while len(to_explore) > 0:
            pos_to = to_explore.pop()
            if pos == pos_to:
                continue

            # find a way to go to destination
            path = dijkstra(grid, pos, pos_to)
            for cmd in path[:-1]:
                input_l[0] = cmd
                if not next(computer) in [1, 2]:
                    raise NotImplementedError("Unexpected value from the computer.")
                pos = pos_add(pos, DIRECTIONS[cmd])
            cmd = path[-1]
            input_l[0] = cmd
            out = next(computer)
            next_pos = pos_add(pos, DIRECTIONS[cmd])

            # update grid and position
            if out == 0:
                grid[next_pos] = 0
            elif out == 1:
                pos = next_pos
                grid[next_pos] = 1
            elif out == 2:
                pos = next_pos
                grid[next_pos] = 1
                pos_oxygen = pos
            else:
                raise NotImplementedError("Unexpected value from the computer. (-1)")
            
            # update to_explore and seen
            for d in DIRECTIONS.values():
                to_explore_pos = pos_add(pos, d)
                if not to_explore_pos in seen:
                    seen.add(to_explore_pos)
                    to_explore.append(to_explore_pos)

        return dijkstra_maxdist(grid, pos_oxygen)

def dijkstra_maxdist(grid, pos_from):
    max_dist = 0
    to_visit = collections.deque([(pos_from, 0)])
    seen = {pos_from}

    while len(to_visit) > 0:
        u, dist = to_visit.popleft()
        max_dist = max(max_dist, dist)

        for cmd in range(1, 4+1):
            v = pos_add(u, DIRECTIONS[cmd])
            if v in seen:
                continue
            seen.add(v)
            if not grid.get(v, 0) == 0:
                to_visit.append((v, dist+1))
    
    return max_dist


def dijkstra(grid, pos_from, pos_to):
    prev = {pos_from: None}
    to_visit = collections.deque([pos_from])

    while len(to_visit) > 0:
        u = to_visit.popleft()
        for cmd in range(1, 4+1):
            v = pos_add(u, DIRECTIONS[cmd])
            if v in prev:
                continue
            prev[v] = (u, cmd)
            if v == pos_to:
                return make_path(pos_from, pos_to, prev)
            if not grid.get(v, 0) == 0:
                to_visit.append(v)


def make_path(pos_from, pos_to, prev):
    path = []
    v = pos_to
    while v != pos_from:
        u, cmd = prev[v]
        path.append(cmd)
        v = u
    return path[::-1]


def pos_add(pos1, pos2):
    (x1, y1), (x2, y2) = pos1, pos2
    return (x1+x2, y1+y2)

tile_repr = {
    -1: " ",
    0: "#",
    1: ".",
}

def print_map(map, robot=None):
    xmin = min(x for x, _ in map.keys()) - 1
    xmax = max(x for x, _ in map.keys()) + 1
    ymin = min(y for _, y in map.keys()) - 1
    ymax = max(y for _, y in map.keys()) + 1

    s = ""
    for y in range(ymax, ymin-1, -1):
        for x in range(xmin, xmax+1):
            if (x, y) == robot:
                s += 'R'
            else:
                s += tile_repr[map.get((x, y), -1)]
        s += "\n"

    print(s)

def compute(code, input_l):
    p = collections.defaultdict(int, enumerate(code))
    pc = 0
    relative_base = 0

    def index(pos):
        mode = (p[pc] // 10 ** (1 + pos)) % 10
        if mode == 0:
            return p[pc + pos]
        if mode == 1:
            return pc + pos
        if mode == 2:
            return relative_base + p[pc + pos]
        raise Exception("Bad param mode")

    while True:
        op = p[pc] % 100

        if op == 1:
            p[index(3)] = p[index(1)] + p[index(2)]
            pc += 4
        elif op == 2:
            p[index(3)] = p[index(1)] * p[index(2)]
            pc += 4
        elif op == 3:
            p[index(1)] = input_l[0]
            pc += 2
        elif op == 4:
            yield p[index(1)]
            pc += 2
        elif op == 5:
            pc = p[index(2)] if p[index(1)] != 0 else pc + 3
        elif op == 6:
            pc = p[index(2)] if p[index(1)] == 0 else pc + 3
        elif op == 7:
            p[index(3)] = 1 if p[index(1)] < p[index(2)] else 0
            pc += 4
        elif op == 8:
            p[index(3)] = 1 if p[index(1)] == p[index(2)] else 0
            pc += 4
        elif op == 9:
            relative_base += p[index(1)]
            pc += 2
        elif op == 99:
            break
        else:
            raise Exception("Unknown op code")
