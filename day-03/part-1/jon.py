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
        points_a = set(points(lines[0]))
        points_b = set(points(lines[1]))
        return min(abs(x) + abs(y) for x, y in points_a.intersection(points_b))


def points(line):
    posx, posy = 0, 0
    for elem in line.split(","):
        dirx, diry = directions[elem[:1]]
        for _ in range(int(elem[1:])):
            posx, posy = posx + dirx, posy + diry
            yield (posx, posy)
