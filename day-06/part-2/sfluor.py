from collections import defaultdict, deque
from tool.runners.python import SubmissionPy


def dfs(graph, start="COM"):
    queue = deque()

    queue.append((0, start))

    while queue:
        depth, curr = queue.pop()
        childs = graph[curr]

        for child in childs:
            queue.append((depth + 1, child))
            yield (child, depth + 1)


def upward(iv_graph, node):
    curr = iv_graph[node]

    while True:
        if curr not in iv_graph:
            break
        yield curr
        curr = iv_graph[curr]


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here

        graph = defaultdict(list)
        iv_graph = {}

        for center, orb in (line.split(")") for line in s.splitlines()):
            graph[center].append(orb)
            iv_graph[orb] = center

        depths = {k: v for k, v in dfs(graph)}

        s1 = set(upward(iv_graph, "YOU"))
        s2 = set(upward(iv_graph, "SAN"))

        depth, father = max((depths[n], n) for n in (s1 & s2))

        return depths["YOU"] + depths["SAN"] - 2 * (depth + 1)
