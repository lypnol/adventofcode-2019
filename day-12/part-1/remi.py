from tool.runners.python import SubmissionPy


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
            planets.append((x, y, z))
            velocity.append((0, 0, 0))

        for step in range(1000):

            gravity = [(0, 0, 0)] * len(planets)

            for i, planet1 in enumerate(planets):
                for j, planet2 in enumerate(planets):
                    if i == j:
                        continue
                    ax, ay, az = gravity[j]
                    if planet1[0] > planet2[0]:
                        ax += 1
                    elif planet1[0] < planet2[0]:
                        ax += -1

                    if planet1[1] > planet2[1]:
                        ay += 1
                    elif planet1[1] < planet2[1]:
                        ay += -1

                    if planet1[2] > planet2[2]:
                        az += 1
                    elif planet1[2] < planet2[2]:
                        az += -1

                    gravity[j] = (ax, ay, az)

            for i in range(len(planets)):
                ax, ay, az = gravity[i]

                vx, vy, vz = velocity[i]
                velocity[i] = (vx + ax, vy + ay, vz + az)
                vx, vy, vz = velocity[i]

                x, y, z = planets[i]
                planets[i] = (x + vx, y + vy, z + vz)

        energy = 0

        for i in range(len(planets)):
            x, y, z = planets[i]
            vx, vy, vz = velocity[i]

            pot = abs(x) + abs(y) + abs(z)
            kin = abs(vx) + abs(vy) + abs(vz)

            energy += pot * kin

        return energy

