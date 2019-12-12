from tool.runners.python import SubmissionPy


import math


def parse_grid(s):
    return [
        (x, y)
        for x, line in enumerate(s.splitlines())
        for y, char in enumerate(line.strip())
        if char == "#"
    ]


def direction(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    d = math.gcd(delta_x, delta_y)
    return delta_x // d, delta_y // d


def seeable(grid, x1, y1):
    directions = set()
    for (x2, y2) in grid:
        if (x1, y1) != (x2, y2):
            directions.add(direction(x1, y1, x2, y2))
    return len(directions)


def solve_part1(grid):
    return max(
        ((x, y) for (x, y) in grid), key=lambda pos: seeable(grid, pos[0], pos[1]),
    )


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        grid = parse_grid(s)
        (x1, y1) = solve_part1(grid)
        return seeable(grid, x1, y1)
