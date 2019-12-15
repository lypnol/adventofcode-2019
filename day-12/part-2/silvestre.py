import math
from functools import reduce
from tool.runners.python import SubmissionPy

def lcm(a, b):
    return a * b // math.gcd(a, b)

class SilvestreSubmission(SubmissionPy):

    @staticmethod
    def parse_line(l):
        """<x=-4, y=3, z=15>"""
        return [int(el.strip()[2:]) for el in l[1:-1].split(",")]

    def run(self, s):
        positions = [self.parse_line(l) for l in  s.strip().splitlines()]
        n_moons = len(positions)
        velocities = [[0,0,0] for _ in range(n_moons)]

        results = []

        # for each dimension
        for d in range(3):
            pos_d = [p[d] for p in positions]
            vel_d = [v[d] for v in velocities]

            k = 0
            seen_state = {}
            while True:
                state = (tuple(pos_d), tuple(vel_d))

                if state in seen_state:
                    results.append(k)
                    break
                else:
                    seen_state[state] = k
                    k += 1
                    
                # apply gravity
                for i in range(n_moons):
                    for j in range(i+1, n_moons):
                        if pos_d[i] > pos_d[j]:
                            vel_d[i] -= 1
                            vel_d[j] += 1
                        elif pos_d[i] < pos_d[j]:
                            vel_d[i] += 1
                            vel_d[j] -= 1
            
                # apply velocity
                for i in range(n_moons):
                    pos_d[i] += vel_d[i]


        return reduce(lcm, results)