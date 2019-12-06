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
            yield depth + 1


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here

        graph = defaultdict(list)

        for center, orb in (line.split(")") for line in s.splitlines()):
            graph[center].append(orb)

        return sum(dfs(graph))
