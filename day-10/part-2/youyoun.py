from tool.runners.python import SubmissionPy
from collections import Counter, defaultdict


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Asteroid):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"


def compute_slope(origin: Asteroid, ast: Asteroid):
    if ast.x == origin.x:
        return float("inf")
    elif ast.y == origin.y:
        return 0
    else:
        return (ast.y - origin.y) / (ast.x - origin.x)


def compute_direction(origin: Asteroid, ast: Asteroid):
    if ast.x == origin.x:
        return (ast.y - origin.y) / abs(ast.y - origin.y)
    elif ast.y == origin.y:
        return (ast.x - origin.x) / abs(ast.x - origin.x)
    else:
        return (ast.x - origin.x) / abs(ast.x - origin.x)


def distance(origin: Asteroid, ast: Asteroid):
    return (origin.y - ast.y) ** 2 + (origin.x - ast.x) ** 2


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # Parse input
        coords = set({})
        for j, line in enumerate(s.splitlines()):
            for i in range(len(line)):
                if line[i] == "#":
                    coords.add(Asteroid(i, j))

        monitor = None
        monitor_slopes_ast_map = {}
        max_monitored = 0
        for mon in coords:
            slope_asts_map = defaultdict(set)
            for ast in coords:
                if mon == ast:
                    continue
                slope = compute_slope(mon, ast)
                dir = compute_direction(mon, ast)
                slope_asts_map[(slope, dir)].add(ast)
            n_monitored = len(slope_asts_map)
            if n_monitored > max_monitored:
                monitor = mon
                max_monitored = n_monitored
                monitor_slopes_ast_map = {}
                for s in slope_asts_map:
                    monitor_slopes_ast_map[s] = sorted(slope_asts_map[s], key=lambda x: -distance(mon, x))

        slopes_pos_dir = sorted([s for s in monitor_slopes_ast_map if s[1] > 0], key=lambda x: x[0])
        slopes_neg_dir = sorted([s for s in monitor_slopes_ast_map if s[1] < 0], key=lambda x: x[0])
        start = slopes_neg_dir.pop()
        sorted_slopes = [start] + slopes_pos_dir + slopes_neg_dir

        i = 0
        remaining_asts = max_monitored
        processed_slopes = set()
        while True:
            if sorted_slopes[i] in processed_slopes:
                continue
            destroyed = monitor_slopes_ast_map[sorted_slopes[i]].pop()
            if len(monitor_slopes_ast_map[sorted_slopes[i]]) == 0:
                processed_slopes.add(sorted_slopes[i])
            remaining_asts -= 1
            if remaining_asts == max_monitored - 200:
                return destroyed.x * 100 + destroyed.y
            if i >= len(sorted_slopes):
                i = 0
            else:
                i += 1
