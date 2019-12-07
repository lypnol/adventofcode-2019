from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def run(self, s):
        planets = dict()
        for orbit in s.split("\n"):
            center, orbiter = orbit.split(")")

            center = planets.setdefault(center, Planet(center))
            orbiter = planets.setdefault(orbiter, Planet(orbiter))
            orbiter.orbit = center

        return sum(planet.count_orbits() for planet in planets.values())


class Planet:
    def __init__(self, name, orbit=None):
        self.name = name
        self.orbit = orbit

    def count_orbits(self):
        if self.orbit is not None:
            return 1 + self.orbit.count_orbits()
        else:
            return 0
