from tool.runners.python import SubmissionPy


def get_coords(steps):
    x, y = 0, 0
    coords = set()
    for step in steps.split(","):
        if step[0] == "R":
            for i in range(x, x + int(step[1:])):
                coords.add((i, y))
            x = x + int(step[1:])
        elif step[0] == "L":
            for i in range(x, x - int(step[1:]), -1):
                coords.add((i, y))
            x = x - int(step[1:])
        elif step[0] == "D":
            for i in range(y, y - int(step[1:]), -1):
                coords.add((x, i))
            y = y - int(step[1:])
        elif step[0] == "U":
            for i in range(y, y + int(step[1:])):
                coords.add((x, i))
            y = y + int(step[1:])
    return coords


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        l1, l2 = s.splitlines()
        d1 = get_coords(l1)
        d2 = get_coords(l2)
        intersections = d2.intersection(d1) - {(0, 0)}
        return min([abs(e[0]) + abs(e[1]) for e in intersections])
