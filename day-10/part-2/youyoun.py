from tool.runners.python import SubmissionPy
from collections import defaultdict


def distance(origin, ast):
    return (origin[1] - ast[1]) ** 2 + (origin[0] - ast[0]) ** 2


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # Parse input
        coords = set({})
        for j, line in enumerate(s.splitlines()):
            for i in range(len(line)):
                if line[i] == "#":
                    coords.add((i, j))

        monitor_slopes_ast_map = {}
        max_monitored = 0
        for mon in coords:
            slope_asts_map = defaultdict(set)
            for ast in coords:
                if mon == ast:
                    continue
                if mon[0] == ast[0]:
                    slope = 1000000
                    dir = (ast[1] - mon[1]) / abs(ast[1] - mon[1])
                else:
                    slope = (ast[1] - mon[1]) / (ast[0] - mon[0])
                    dir = (ast[0] - mon[0]) / abs(ast[0] - mon[0])
                slope_asts_map[(slope, dir)].add(ast)
            n_monitored = len(slope_asts_map)
            if n_monitored > max_monitored:
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
                return destroyed[0] * 100 + destroyed[1]
            if i >= len(sorted_slopes):
                i = 0
            else:
                i += 1
