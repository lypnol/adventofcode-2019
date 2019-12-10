from collections import defaultdict
from tool.runners.python import SubmissionPy
from typing import Dict, List, Tuple


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Parse input
        orbits = list(map(self.parse_orbit_string, s.strip().splitlines()))

        # Build direct orbit tree
        direct_orbit_tree: Dict[str, List[str]] = defaultdict(list)
        for inner, outer in orbits:
            direct_orbit_tree[inner].append(outer)

        # Build indirect orbit tree ( virtually, because in the end we only extract metadata from it )
        _, result = self.extract_number_of_descendants("COM", direct_orbit_tree)

        # Return result
        return result

    def parse_orbit_string(self, string: str) -> Tuple[str, str]:
        inner, outer = string.split(")")
        return (inner, outer)

    def extract_number_of_descendants(
        self, node: str, direct_orbit_tree: Dict[str, List[str]]
    ) -> Tuple[int, int]:
        """
        Return:
            - total number of descendants of the node
            - cumsum of the total number of descendants of the node
        """
        total = 0
        cumsum = 0

        for child in direct_orbit_tree[node]:
            sub_total, sub_cumsum = self.extract_number_of_descendants(
                child, direct_orbit_tree
            )
            total += 1 + sub_total  # child + children of the child
            cumsum += sub_cumsum

        cumsum += total

        return total, cumsum
