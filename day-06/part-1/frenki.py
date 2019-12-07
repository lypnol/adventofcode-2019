from tool.runners.python import SubmissionPy
from collections import defaultdict, deque

class FrenkiSubmission(SubmissionPy):

    def run(self, s):
        orbits = defaultdict(list)
        l = list(map(lambda x: x.split(')'), s.splitlines()))
        for i in l:
            orbits[i[0]].append(i[1])

        to_visit = deque()
        to_visit.append(('COM', 0))
        res = 0
        while to_visit:
            planet, v = to_visit.pop()
            res += v
            for i in orbits[planet]:
                to_visit.append((i, v+1))
        return res