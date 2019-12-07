from tool.runners.python import SubmissionPy

from collections import deque

class FranciscoSubmission(SubmissionPy):

    @staticmethod
    def lines_to_graph_part2(lines):
        graph = dict()
        for line in lines:
            a, b = line.strip().split(")")
            graph[a] = graph.get(a, [])
            graph[b] = graph.get(b, [])
            graph[b].append(a)
            graph[a].append(b)
        return graph

    @staticmethod
    def solve_part2(graph):
        q = deque([("YOU", 0)])
        seen = {"YOU"}
        while q:
            node, l = q.popleft()
            for neighbor in graph[node]:
                if neighbor == "SAN":
                    return l - 1
                elif neighbor not in seen:
                    seen.add(neighbor)
                    q.append((neighbor, l+1))

    def run(self, s):
        return self.solve_part2(self.lines_to_graph_part2(s.splitlines()))
