from functools import lru_cache
from tool.runners.python import SubmissionPy


def parse_orbits(s):
    return {r.split(")")[1]: r.split(")")[0] for r in s.splitlines()}


def get_path_to_root(parents, node, root):
    res = [node]
    while res[-1] != root:
        res.append(parents[res[-1]])
    return res


def get_number_of_transfers(orbit_around, src, dest):
    com_to_src = get_path_to_root(orbit_around, src, "COM")[::-1]
    com_to_dest = get_path_to_root(orbit_around, dest, "COM")[::-1]
    src_depth = len(com_to_src) - 1
    dest_depth = len(com_to_dest) - 1
    for depth in range(min(src_depth, dest_depth) + 1):
        if com_to_src[depth] != com_to_dest[depth]:
            common_ancestor_depth = depth - 1
            src_to_common_ancestor_transfers = src_depth - common_ancestor_depth
            common_ancestor_to_dest_transfers = dest_depth - common_ancestor_depth
            return src_to_common_ancestor_transfers + common_ancestor_to_dest_transfers
    raise "No path found"


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        orbit_around = parse_orbits(s)
        return get_number_of_transfers(
            orbit_around, orbit_around["YOU"], orbit_around["SAN"]
        )
