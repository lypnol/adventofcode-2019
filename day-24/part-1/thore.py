import copy

from tool.runners.python import SubmissionPy

BUG = "#"
EMPTY = "."


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        world = parse_input(s)
        seen_states = set()

        while True:
            seen_states.add(str(world))
            world = step(world)
            if str(world) in seen_states:
                break

        return biodiversity_rating(world)


def parse_input(s):
    lines = s.replace(BUG, "1").replace(EMPTY, "0").splitlines()
    return [[int(c) for c in line] for line in lines]


def step(world):
    n, p = len(world), len(world[0])
    new_world = copy.deepcopy(world)

    for i in range(n):
        for j in range(n):
            n_bugs = sum(world[i_n][j_n] for i_n, j_n in get_neighbours(world, i, j))

            if world[i][j] == 1 and n_bugs != 1:
                new_world[i][j] = 0

            elif world[i][j] == 0 and n_bugs in [1, 2]:
                new_world[i][j] = 1

    return new_world


def get_neighbours(world, i, j):
    n, p = len(world), len(world[0])
    if i - 1 >= 0:
        yield i - 1, j
    if j - 1 >= 0:
        yield i, j - 1
    if i + 1 < n:
        yield i + 1, j
    if j + 1 < p:
        yield i, j + 1


def biodiversity_rating(world):
    return int(
        "".join(("".join(str(c) for c in reversed(line)) for line in reversed(world))),
        2,
    )


def pprint_world(world):
    print("\n".join("".join(BUG if c == 1 else EMPTY for c in line) for line in world))
    print()

