from tool.runners.python import SubmissionPy
import math


class JonSubmission(SubmissionPy):

    def run(self, s):
        lines = s.strip().split("\n")

        pos = []
        for l in lines:
            pos.append([int(p.strip().split("=")[1]) for p in l.strip("<>").split(",")])

        n = len(pos)
        vel = [[0, 0, 0] for _ in range(n)]
        r = []

        for d in range(3):

            pos_d = [p[d] for p in pos]
            vel_d = [v[d] for v in vel]

            states = {}
            step = 0

            while True:
                state = (tuple(pos_d), tuple(vel_d))

                if state in states:
                    if states[state] != 0:
                        raise Exception("Not looping back on the initial state")
                    r.append(step)
                    break

                states[state] = step
                step += 1

                sim_step(pos_d, vel_d)

        return lcm(r[0], lcm(r[1], r[2]))


def sim_step(pos, vel):
    for i in range(4):
        for j in range(i + 1, 4):
            if pos[i] < pos[j]:
                vel[i] += 1
                vel[j] -= 1
            elif pos[i] > pos[j]:
                vel[i] -= 1
                vel[j] += 1

    for i in range(4):
        pos[i] += vel[i]


def lcm(a, b):
    return a*b // math.gcd(a, b)
