from tool.runners.python import SubmissionPy
from typing import Dict, List, Tuple


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag

        # Parse input
        orbits = list(map(self.parse_orbit_string, s.strip().splitlines()))

        # Build direct orbit tree
        reverse_direct_orbit_tree: Dict[str, str] = dict()
        for inner, outer in orbits:
            reverse_direct_orbit_tree[outer] = inner

        # Find path from YOU to COM
        you_to_com: List[str] = list()
        node = "YOU"
        while node != "COM":
            node = reverse_direct_orbit_tree[node]
            you_to_com.append(node)

        # Find path from SAN to COM
        san_to_com: List[str] = list()
        node = "SAN"
        while node != "COM":
            node = reverse_direct_orbit_tree[node]
            san_to_com.append(node)

        # Find the longest suffix
        for idx in range(min(len(you_to_com), len(san_to_com))):
            orbit_alpha = you_to_com[-idx - 1]
            orbit_beta = san_to_com[-idx - 1]

            if orbit_alpha != orbit_beta:
                break

        # Return result
        return len(you_to_com) + len(san_to_com) - 2 * idx

    def parse_orbit_string(self, string: str) -> Tuple[str, str]:
        inner, outer = string.split(")")
        return (inner, outer)
