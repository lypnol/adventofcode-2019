import re
import numpy as np

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        moons = [
            tuple([int(m) for m in re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line).groups()])
            for line in s.splitlines()
        ]
        initial_moons = list(moons)
        velocities = [(0, 0, 0)] * len(moons)
        lcm = {}

        i = 1
        while True:
            for fid, first in enumerate(moons):
                for sid, second in enumerate(moons[(fid + 1):]):
                    real_sid = fid + sid + 1
                    dx = 1 if first[0] < second[0] else (0 if first[0] == second[0] else -1)
                    dy = 1 if first[1] < second[1] else (0 if first[1] == second[1] else -1)
                    dz = 1 if first[2] < second[2] else (0 if first[2] == second[2] else -1)
                    velocities[fid] = (
                        velocities[fid][0] + dx, velocities[fid][1] + dy, velocities[fid][2] + dz
                    )
                    velocities[real_sid] = (
                        velocities[real_sid][0] - dx, velocities[real_sid][1] - dy, velocities[real_sid][2] - dz
                    )

            for idx, moon in enumerate(moons):
                vel = velocities[idx]
                moons[idx] = (moon[0] + vel[0], moon[1] + vel[1], moon[2] + vel[2])

            for k in range(3):
                if [[moon[k] for moon in moons], [vel[k] for vel in velocities]] == \
                        [[m[k] for m in initial_moons], [0, 0, 0, 0]]:
                    if k not in lcm:
                        lcm[k] = i

            if len(lcm) == 3:
                break

            i += 1

        return np.lcm.reduce(list(lcm.values()))
