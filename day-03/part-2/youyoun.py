from tool.runners.python import SubmissionPy


def get_coords(steps):
    x, y = 0, 0
    coords = []
    for step in steps.split(","):
        if step[0] == "R":
            for i in range(x, x + int(step[1:])):
                coords.append((i, y))
            x = x + int(step[1:])
        elif step[0] == "L":
            for i in range(x, x - int(step[1:]), -1):
                coords.append((i, y))
            x = x - int(step[1:])
        elif step[0] == "D":
            for i in range(y, y - int(step[1:]), -1):
                coords.append((x, i))
            y = y - int(step[1:])
        elif step[0] == "U":
            for i in range(y, y + int(step[1:])):
                coords.append((x, i))
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
        intersections = set(d2).intersection(set(d1)) - {(0, 0)}
        min_cost = float('inf')
        for p in intersections:
            cost = d1.index(p) + d2.index(p)
            if cost < min_cost:
                min_cost = cost
        return min_cost
