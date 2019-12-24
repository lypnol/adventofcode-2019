from collections import defaultdict
import copy

from tool.runners.python import SubmissionPy

BUG = "#"
EMPTY = "."
MINUTES = 200


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        world = parse_input(s)

        for minute in range(MINUTES):
            world = step(world)

        # pprint_world_rec(world)
        return count_bugs(world)


def parse_input(s):
    lines = s.replace(BUG, "1").replace(EMPTY, "0").splitlines()

    n, p = len(lines), len(lines[0])
    assert n % 2 == 1 and p % 2 == 1
    world = defaultdict(lambda: [[0 for _ in range(n)] for _ in range(p)])
    world[0] = [[int(c) for c in line] for line in lines]

    return world


def step(world):
    n, p = len(world[0]), len(world[0][0])
    new_world = copy.deepcopy(world)
    levels = list(world.keys())
    for level in levels + [min(levels) - 1, max(levels) + 1]:
        for i in range(n):
            for j in range(p):
                if (i, j) == (n // 2, p // 2):
                    continue
                n_bugs = sum(
                    world[level_n][i_n][j_n]
                    for level_n, i_n, j_n in get_neighbours(world, level, i, j)
                )
                if world[level][i][j] == 1 and n_bugs != 1:
                    new_world[level][i][j] = 0
                elif world[level][i][j] == 0 and n_bugs in [1, 2]:
                    new_world[level][i][j] = 1
    prune(new_world)
    return new_world


def prune(world):
    n, p = len(world[0]), len(world[0][0])
    empty = str([[0 for _ in range(p)] for _ in range(n)])

    finished = False
    while not finished:
        finished = True
        levels = list(world.keys())
        min_level, max_level = min(levels), max(levels)
        if str(world[min_level]) == empty:
            del world[min_level]
            finished = False
        if str(world[max_level]) == empty:
            del world[max_level]
            finished = False


def get_neighbours(world, level, i, j):
    n, p = len(world[0]), len(world[0][0])

    if i - 1 >= 0:
        if (i - 1, j) == (n // 2, p // 2):
            for jj in range(p):
                yield level + 1, n - 1, jj
        else:
            yield level, i - 1, j
    else:
        yield level - 1, 1, p // 2

    if j - 1 >= 0:
        if (i, j - 1) == (n // 2, p // 2):
            for ii in range(n):
                yield level + 1, ii, p - 1
        else:
            yield level, i, j - 1
    else:
        yield level - 1, n // 2, 1

    if i + 1 < n:
        if (i + 1, j) == (n // 2, p // 2):
            for jj in range(p):
                yield level + 1, 0, jj
        else:
            yield level, i + 1, j
    else:
        yield level - 1, n // 2 + 1, p // 2

    if j + 1 < p:
        if (i, j + 1) == (n // 2, p // 2):
            for ii in range(n):
                yield level + 1, ii, 0
        else:
            yield level, i, j + 1
    else:
        yield level - 1, n // 2, p // 2 + 1


def count_bugs(world):
    return sum(
        sum(sum(world[level][i]) for i in range(len(world[0])))
        for level in world.keys()
    )


def pprint_world(world):
    print("\n".join("".join(BUG if c == 1 else EMPTY for c in line) for line in world))
    print()


def pprint_world_rec(world):
    for level in sorted(world.keys()):
        print(f"Depth {level}:")
        pprint_world(world[level])
