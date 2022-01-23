from tool.runners.python import SubmissionPy

from collections import deque


class ThChSubmission(SubmissionPy):
    def run(self, s):
        #         s = """
        # COM)B
        # B)C
        # C)D
        # D)E
        # E)F
        # B)G
        # G)H
        # D)I
        # E)J
        # J)K
        # K)L
        # """.strip()
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        orbits = {}
        for orbit in s.splitlines():
            orbitted, orbitting = orbit.split(")")
            orbits[orbitting] = orbitted

        nb_of_orbits_by_object = {"COM": 0}
        to_process = deque(orbits.keys())
        while to_process:
            orbitting = to_process.popleft()
            if orbitting in nb_of_orbits_by_object:
                continue

            orbitted = orbits[orbitting]
            if orbitted not in nb_of_orbits_by_object:
                to_process.appendleft(orbitting)
                to_process.appendleft(orbitted)
            else:
                nb_of_orbits_by_object[orbitting] = 1 + nb_of_orbits_by_object[orbitted]

        return sum(nb_of_orbits_by_object.values())
