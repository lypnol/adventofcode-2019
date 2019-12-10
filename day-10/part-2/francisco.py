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

def angle(x, y):
    # an angle is made of 2 parts
    # - the quadrant of the place it's in (between 1 and 4)
    # - the angle itself, between 0 and infinite
    if x >= 0 and y > 0:
        return (1, abs(x/y))
    elif x > 0 and y <= 0:
        return (2, abs(y/x))
    elif x <= 0 and y < 0:
        return (3, abs(x/y))
    elif x < 0 and y >= 0:
        return (4, abs(y/x))

def sorted_asteroids(grid, x1, y1):
    asteroids = dict()

    for x2 in range(len(grid)):
        for y2 in range(len(grid[0])):
            if (x1, y1) != (x2, y2) and grid[x2][y2]:
                x, y = x2-x1, y2-y1
                a = angle(y, -x)
                a = (a[0], int(a[1] * 10e10))
                if a not in asteroids:
                    asteroids[a] = []
                asteroids[a].append((abs(x2-x1)+abs(y2-y1), (x2, y2)))

    for l in asteroids.values():
        l.sort()
        l.reverse()

    return asteroids

def solve_part2(grid, x, y):
    asteroids = sorted_asteroids(grid, x, y)
    angles = sorted(asteroids)
    i = 1
    popped = []
    while max(len(l) for l in asteroids.values()) > 0:
        for a in angles:
            if len(asteroids[a]) > 0:
                dist, coords = asteroids[a].pop()
                popped.append(coords)
                i += 1

    return popped

class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        grid = parse_grid(s)
        (x1, y1) = solve_part1(grid)
        (x2, y2) = solve_part2(grid, x1, y1)[199]
        return 100 * y2 + x2
