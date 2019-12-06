from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def run(self, s):
        planets = dict()
        for orbit in s.split("\n"):
            center, orbiter = orbit.split(")")

            center = planets.setdefault(center, Planet(center))
            orbiter = planets.setdefault(orbiter, Planet(orbiter))
            orbiter.orbit = center

        you_chain = planets["YOU"].orbit_chain()
        san_chain = planets["SAN"].orbit_chain()

        i = 0
        while you_chain[i] in san_chain:
            i += 1
        common_ancester = i

        return len(you_chain) - common_ancester + len(san_chain) - common_ancester


class Planet:
    def __init__(self, name, orbit=None):
        self.name = name
        self.orbit = orbit

    def count_orbits(self):
        if self.orbit is not None:
            return 1 + self.orbit.count_orbits()
        else:
            return 0

    def orbit_chain(self):
        if self.orbit is not None:
            ch = self.orbit.orbit_chain()
            ch.append(self.orbit)
            return ch
        else:
            return []
