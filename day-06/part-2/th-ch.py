from tool.runners.python import SubmissionPy

from collections import defaultdict
from queue import PriorityQueue


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
        # K)YOU
        # I)SAN
        # """.strip()
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        orbits = {}
        for orbit in s.splitlines():
            orbitted, orbitting = orbit.split(")")
            orbits[orbitting] = orbitted

        reversed_orbits = defaultdict(list)
        for b, a in orbits.items():
            reversed_orbits[a].append(b)

        # Dijkstra
        D = {orbit: float("inf") for orbit in ["COM"] + list(orbits.keys())}
        start_vertex = orbits["YOU"]
        D[start_vertex] = 0

        pq = PriorityQueue()
        pq.put((0, start_vertex))
        visited = set()

        while not pq.empty():
            (dist, current_orbit) = pq.get()
            visited.add(current_orbit)

            for neighbor in [orbits.get(current_orbit)] + reversed_orbits.get(
                current_orbit, []
            ):
                if neighbor is None:
                    continue

                distance = 1
                if neighbor not in visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_orbit] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost

        return D[orbits["SAN"]]
