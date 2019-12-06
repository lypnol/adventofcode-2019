from tool.runners.python import SubmissionPy

import functools

class FranciscoSubmission(SubmissionPy):

    @staticmethod
    def lines_to_graph_part1(lines):
        graph = dict()
        for line in lines:
            a, b = line.strip().split(")")
            graph[a] = graph.get(a, [])
            graph[b] = graph.get(b, [])
            graph[b].append(a)
        return graph

    @staticmethod
    def solve_part1(graph):

        @functools.lru_cache(maxsize=None)
        def count_children(node):
            return len(graph[node]) + sum(count_children(child) for child in graph[node])

        return sum(count_children(node) for node in graph)

    def run(self, s):
        return self.solve_part1(self.lines_to_graph_part1(s.splitlines()))
