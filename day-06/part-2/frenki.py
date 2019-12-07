from tool.runners.python import SubmissionPy
from collections import defaultdict, deque

class FrenkiSubmission(SubmissionPy):

    def run(self, s):
        orbits = defaultdict(list)
        l = list(map(lambda x: x.split(')'), s.splitlines()))
        for i in l:
            if i[1] == 'YOU':
                start = i[0]
            if i[1] == 'SAN':
                end = i[0]
            orbits[i[0]].append(i[1])
            orbits[i[1]].append(i[0])

        to_visit = deque()
        to_visit.append((start, 0))
        visited = defaultdict(bool)
        while to_visit:
            planet, v = to_visit.pop()
            visited[planet] = True
            if planet == end:
                return v
            for i in orbits[planet]:
                if not visited[i]:
                    to_visit.append((i, v+1))