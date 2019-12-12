from tool.runners.python import SubmissionPy

from collections import deque, defaultdict


def lines_to_graph_part1(lines):
    graph = defaultdict(lambda: [])
    for line in lines:
        a, b = line.strip().split(")")
        graph[a].append(b)
    return graph


def solve_part1(graph):
    q = deque([("COM", 0)])
    total_parents = 0

    while q:
        node, parents = q.popleft()
        total_parents += parents
        for child in graph[node]:
            q.append((child, parents + 1))

    return total_parents


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part1(lines_to_graph_part1(s.splitlines()))
