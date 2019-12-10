from tool.runners.python import SubmissionPy


import math


def parse_grid(s):
    return [[char == "#" for char in line.strip()] for line in s.splitlines()]


def direction(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    d = math.gcd(delta_x, delta_y)
    return delta_x // d, delta_y // d


def seeable(grid, x1, y1):
    directions = set()
    for x2 in range(len(grid)):
        for y2 in range(len(grid[0])):
            if (x1, y1) != (x2, y2) and grid[x2][y2]:
                directions.add(direction(x1, y1, x2, y2))
    return len(directions)


def solve_part1(grid):
    return max(
        ((x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y]),
        key = lambda pos: seeable(grid, pos[0], pos[1])
    )

class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        grid = parse_grid(s)
        (x1, y1) = solve_part1(grid)
        return seeable(grid, x1, y1)
