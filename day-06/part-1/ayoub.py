from collections import defaultdict
from tool.runners.python import SubmissionPy


def _explore(g, start):
    Q = [(start, 0)]
    res = 0
    seen = set()
    while Q:
        current, lvl = Q.pop()
        res += lvl
        seen.add(current)
        for child in g[current]:
            if child not in seen:
                Q.append((child, lvl+1))
    return res


class AyoubSubmission(SubmissionPy):
    def run(self, s):
        g = defaultdict(list)
        for l in s.split('\n'):
            a, b = l.strip().split(')')
            g[a].append(b)
        return _explore(g, 'COM')
