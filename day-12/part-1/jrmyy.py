import re

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        moons = [
            tuple([int(m) for m in re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line).groups()])
            for line in s.splitlines()
        ]
        velocities = [(0, 0, 0)] * len(moons)
        for i in range(1000):
            for fid, first in enumerate(moons):
                for sid, second in enumerate(moons[(fid + 1):]):
                    real_sid = fid + sid + 1
                    dx = 1 if first[0] < second[0] else (0 if first[0] == second[0] else -1)
                    dy = 1 if first[1] < second[1] else (0 if first[1] == second[1] else -1)
                    dz = 1 if first[2] < second[2] else (0 if first[2] == second[2] else -1)
                    velocities[fid] = (velocities[fid][0] + dx, velocities[fid][1] + dy, velocities[fid][2] + dz)
                    velocities[real_sid] = (
                        velocities[real_sid][0] - dx, velocities[real_sid][1] - dy, velocities[real_sid][2] - dz
                    )

            for idx, moon in enumerate(moons):
                vel = velocities[idx]
                moons[idx] = (moon[0] + vel[0], moon[1] + vel[1], moon[2] + vel[2])

        return sum([
            (abs(moons[i][0]) + abs(moons[i][1]) + abs(moons[i][2])) *
            (abs(velocities[i][0]) + abs(velocities[i][1]) + abs(velocities[i][2]))
            for i in range(len(moons))
        ])
