from tool.runners.python import SubmissionPy

from collections import deque, defaultdict


def lines_to_graph_part2(lines):
    graph = defaultdict(lambda: [])
    for line in lines:
        a, b = line.strip().split(")")
        graph[b].append(a)
        graph[a].append(b)
    return graph


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
                q.append((neighbor, l + 1))


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part2(lines_to_graph_part2(s.splitlines()))
