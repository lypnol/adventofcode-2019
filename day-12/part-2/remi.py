from tool.runners.python import SubmissionPy

from math import gcd


class RemiSubmission(SubmissionPy):
    def run(self, s):

        planets = []
        velocity = []
        for line in s.split("\n"):
            line = line[1:-1]
            (x, y, z) = line.split(",")
            x = int(x.split("=")[1])
            y = int(y.split("=")[1])
            z = int(z.split("=")[1])
            planets.append([x, y, z])
            velocity.append([0, 0, 0])

        stepx = find_period(planets, velocity, 0)
        stepy = find_period(planets, velocity, 1)
        stepz = find_period(planets, velocity, 2)

        p = (stepx * stepy) // gcd(stepx, stepy)

        return (p * stepz) // gcd(p, stepz)


def find_period(planets, velocity, dim):
    init_state = compute_state(planets, velocity, dim)
    step = 0
    state = ()
    while state != init_state:
        step += 1

        gravity = [0] * len(planets)

        for i, planet1 in enumerate(planets):
            for j, planet2 in enumerate(planets):
                if i == j:
                    continue
                a = gravity[j]
                if planet1[dim] > planet2[dim]:
                    a += 1
                elif planet1[dim] < planet2[dim]:
                    a += -1

                gravity[j] = a

        for i in range(len(planets)):
            velocity[i][dim] += gravity[i]

            planets[i][dim] += velocity[i][dim]

        state = compute_state(planets, velocity, dim)

    return step


def compute_state(planets, velocity, i):
    state = ()
    for planet in planets:
        state += (planet[i],)
    for v in velocity:
        state += (v[i],)

    return state
