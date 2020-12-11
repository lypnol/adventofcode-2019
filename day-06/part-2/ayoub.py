from collections import defaultdict
from tool.runners.python import SubmissionPy


def _min_dist(g, start, end):
    d = defaultdict(lambda: float('inf'))
    d[start] = 0
    Q = [(start, 0)]
    while Q:
        current, dis = Q.pop()
        for child in g[current]:
            if d[child] > dis + 1:
                d[child] = dis + 1
                Q.append((child, dis + 1))
    return d[end]


class AyoubSubmission(SubmissionPy):
    def run(self, s):
        g = defaultdict(list)
        for l in s.split('\n'):
            a, b = l.strip().split(')')
            g[a].append(b)
            g[b].append(a)
        return _min_dist(g, 'YOU', 'SAN') - 2
