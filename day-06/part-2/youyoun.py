from tool.runners.python import SubmissionPy
from collections import defaultdict


def find(map, planet_name):
    planets = {(frozenset(), "COM")}
    while len(planets) != 0:
        path, curr_planet = planets.pop()
        if planet_name in map[curr_planet]:
            return path
        for sat in map[curr_planet]:
            new_path = frozenset(path.union({curr_planet}))
            planets.add((new_path, sat))
    return 0

class YouyounSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        orbits = [x.split(")") for x in s.splitlines()]
        orbit_map = defaultdict(set)
        for e in orbits:
            orbit_map[e[0]].add(e[1])
        path_to_you = find(orbit_map, "YOU")
        path_to_san = find(orbit_map, "SAN")
        return len(path_to_san.union(path_to_you) - path_to_san.intersection(path_to_you)) + 2