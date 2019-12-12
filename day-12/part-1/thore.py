from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        N_STEPS = 1000

        planets = parse_planets(s)
        universe = Universe(planets)
        universe.run(N_STEPS)

        return universe.total_energy()


def parse_planets(s):
    planets = []
    for line in s.splitlines():
        vel = [0, 0, 0]
        pos = [int(p.split("=")[-1]) for p in line[1:-1].split(",")]
        planets.append(Planet(pos, vel))
    return planets


class Universe:
    def __init__(self, planets):
        self.planets = planets
        self.n_planets = len(planets)

    def total_energy(self):
        return sum([planet.total_energy() for planet in self.planets])

    def run(self, n_steps, debug_every=None):
        for i in range(n_steps):
            if debug_every is not None and i % debug_every == 0:
                print(f"After {i} steps:")
                print(self)
                print("\n")

            self.step()

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    def apply_gravity(self):
        for i in range(self.n_planets):
            planet = self.planets[i]
            for j in range(i + 1, self.n_planets):
                other_planet = self.planets[j]
                planet.apply_gravity(other_planet)
                other_planet.apply_gravity(planet)

    def apply_velocity(self):
        for planet in self.planets:
            planet.step()

    def __str__(self):
        return "\n".join([str(planet) for planet in self.planets])


class Planet:
    def __init__(self, pos, vel):
        assert len(pos) == len(vel)
        self.pos = pos
        self.vel = vel
        self.n_dim = len(pos)

    def step(self):
        for i in range(len(self.pos)):
            self.pos[i] += self.vel[i]

    def apply_gravity(self, other_planet):
        for k in range(self.n_dim):
            self.vel[k] += sign(other_planet.pos[k] - self.pos[k])

    def potential_energy(self):
        return sum([abs(x) for x in self.pos])

    def kinetic_energy(self):
        return sum([abs(x) for x in self.vel])

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def __str__(self):
        x, y, z = self.pos
        vx, vy, vz = self.vel
        return (
            f"pos=<x={x:3d}, y={y:3d}, z={z:3d}>, vel=<x={vx:3d}, y={vy:3d}, z={vz:3d}>"
        )


def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
