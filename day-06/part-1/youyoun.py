from tool.runners.python import SubmissionPy
from collections import defaultdict


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        orbits = [x.split(")") for x in s.splitlines()]
        orbit_map = defaultdict(set)
        for e in orbits:
            orbit_map[e[0]].add(e[1])
        planets = {(0, "COM")}
        count = 0
        while len(planets) != 0:
            depth, planet = planets.pop()
            for sat in orbit_map[planet]:
                planets.add((depth + 1, sat))
                count += depth + 1
        return count
