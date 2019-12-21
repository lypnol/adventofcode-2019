from tool.runners.python import SubmissionPy
import collections


turn = {
    "^": {
        "<": "L",
        ">": "R",
    },
    ">": {
        "^": "L",
        "v": "R",
    },
    "v": {
        ">": "L",
        "<": "R",
    },
    "<": {
        "v": "L",
        "^": "R",
    },
}

back = {
    "^": "v",
    ">": "<",
    "v": "^",
    "<": ">",
}

deltas = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]
        code[0] = 2

        inputs = []
        computer = compute(code, inputs)

        view = ""
        while not view.endswith("\n\n"):
            view += chr(next(computer))

        l = view.strip().split("\n")
        h = len(l)
        w = len(l[0])

        # print(view)

        routes = {}
        pos = None
        dir = None

        def viz(x, y):
            if x < 0 or y < 0 or x >= w or y >= h:
                return "."
            return l[y][x]

        for y in range(0, h):
            for x in range(0, w):
                if viz(x, y) == ".":
                    continue
                r = set()
                for d, (dx, dy) in deltas.items():
                    if viz(x+dx, y+dy) != ".":
                        r.add(d)

                if l[y][x] in turn:
                    pos = (x, y)
                    dir = l[y][x]

                routes[(x, y)] = r

        commands = []

        def step():
            if isinstance(commands[-1], int):
                commands[-1] += 1
            else:
                commands.append(1)

        while True:
            possibilities = routes[pos] - {back[dir]}
            if len(possibilities) == 0:
                break
            elif len(possibilities) == 3:
                move = dir
            elif len(possibilities) == 1:
                move = possibilities.pop()
            else:
                raise Exception("Multiple possibilities: {}".format(possibilities))
            if move != dir:
                commands.append(turn[dir][move])
                dir = move
            step()
            dx, dy = deltas[move]
            pos = (pos[0] + dx, pos[1] + dy)
            # print("POS:{} DIR:{} ROUTES:{}".format(pos, dir, routes[pos]))

        cmd_str = ",".join(str(v) for v in commands)

        try:
            compress(cmd_str, "", [])
            raise Exception("Not found")
        except Found as e:
            main, functions = e.args

        while len(functions) < 3:
            functions.append("")

        for c in "{}\n{}\n{}\n{}\nn\n".format(main[1:], functions[0], functions[1], functions[2]):
            inputs.append(ord(c))

        last = 0
        for v in computer:
            last = v

        return last


class Found(Exception):
    pass


fnames = "ABC"


def compress(source, main, functions):
    if len(main) > 20:
        return
    if source == "":
        raise Found(main, functions)
    # Try functions
    for i, f in enumerate(functions):
        if source.startswith(f):
            compress(source[len(f)+1:], "{},{}".format(main, fnames[i]), functions)
    # Create new function
    if len(functions) >= 3:
        return
    i = len(functions)
    for k in range(1, 21):
        if source[k] == ",":
            compress(source[k+1:], "{},{}".format(main, fnames[i]), functions + [source[:k]])


def compute(code, inputs):
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

    input_index = 0

    while True:
        op = p[pc] % 100

        if op == 1:
            p[index(3)] = p[index(1)] + p[index(2)]
            pc += 4
        elif op == 2:
            p[index(3)] = p[index(1)] * p[index(2)]
            pc += 4
        elif op == 3:
            p[index(1)] = inputs[input_index]
            input_index += 1
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
