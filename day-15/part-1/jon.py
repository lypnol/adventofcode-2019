from tool.runners.python import SubmissionPy
import collections


# Positive Y is North
directions = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0),
}


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]

        input_l = [0]
        computer = compute(code, input_l)

        # 1: open
        # 0: wall
        map = {(0, 0): 1}
        to_explore = list(directions.values())
        seen = {(0, 0)}
        seen.update(to_explore)

        pos_robot = (0, 0)
        pos_oxygen = None

        while len(to_explore) > 0:
            target = to_explore.pop()
            assert pos_robot != target
            # print_map(map, robot=pos_robot)
            path = dijkstra(map, pos_robot, target)
            assert len(path) > 0
            for cmd in path[:-1]:
                input_l[0] = cmd
                if next(computer) not in (1, 2):
                    raise Exception("Robot hit an unexpected wall")
                pos_robot = pos_add(pos_robot, directions[cmd])
            cmd = path[-1]
            input_l[0] = cmd
            assert pos_add(pos_robot, directions[cmd]) == target
            out = next(computer)
            if out == 0:
                map[target] = 0
            elif out == 1:
                pos_robot = target
                map[target] = 1
            elif out == 2:
                pos_robot = target
                map[target] = 1
                pos_oxygen = target
            else:
                raise Exception("Unexpected output")
            for dir in directions.values():
                pos = pos_add(pos_robot, dir)
                if pos not in seen:
                    seen.add(pos)
                    to_explore.append(pos)

        assert pos_oxygen is not None

        return len(dijkstra(map, (0, 0), pos_oxygen))


def dijkstra(map, pos_from, pos_to):
    # print("dijkstra from={} to={}".format(pos_from, pos_to))
    assert map[pos_from] == 1
    if pos_from == pos_to:
        return []

    parents = {pos_from: None}  # == seen
    to_visit = collections.deque([pos_from])

    while len(to_visit) > 0:
        x, y = to_visit.popleft()

        for cmd in range(1, 5):
            dx, dy = directions[cmd]
            pos = (x + dx, y + dy)
            if pos in parents:
                continue
            parents[pos] = ((x, y), cmd)
            if pos == pos_to:
                return mkpath(parents, pos_from, pos_to)
            if map.get(pos, 0) == 0:
                continue
            to_visit.append(pos)

    raise Exception("No path found")


def mkpath(parents, pos_from, pos_to):
    cmd_path = []
    curr = pos_to
    while curr != pos_from:
        curr, cmd = parents[curr]
        cmd_path.append(cmd)
    cmd_path.reverse()
    return cmd_path


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


def pos_add(a, b):
    return a[0] + b[0], a[1] + b[1]


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
