from functools import lru_cache
from tool.runners.python import SubmissionPy


def parse_orbits(s):
    return {r.split(")")[1]: r.split(")")[0] for r in s.splitlines()}


def get_number_of_orbits(orbit_around):
    @lru_cache(maxsize=None)
    def get_number_of_orbits_for_planet(planet):
        if planet == "COM":
            return 0

        return 1 + get_number_of_orbits_for_planet(orbit_around[planet])

    return sum(
        [get_number_of_orbits_for_planet(planet) for planet in orbit_around.keys()]
    )


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        orbit_around = parse_orbits(s)
        return get_number_of_orbits(orbit_around)
