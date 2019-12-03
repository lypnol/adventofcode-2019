from tool.runners.python import SubmissionPy


directions = {
    "U": (0, 1),
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
}


class JonSubmission(SubmissionPy):

    def run(self, s):
        lines = s.strip().split("\n")

        steps_a = get_steps(lines[0])
        steps_b = get_steps(lines[1])
        points_a = set(steps_a.keys())
        return min(steps_a[p] + steps_b[p] for p in points_a.intersection(steps_b.keys()))


def get_steps(line):
    steps = {}
    step = 0
    for p in points(line):
        step += 1
        if p not in steps:
            steps[p] = step
    return steps


def points(line):
    posx, posy = 0, 0
    for elem in line.split(","):
        dirx, diry = directions[elem[:1]]
        for _ in range(int(elem[1:])):
            posx, posy = posx + dirx, posy + diry
            yield (posx, posy)
