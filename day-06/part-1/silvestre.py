from tool.runners.python import SubmissionPy
from functools import lru_cache

class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        edges_str = s.split("\n")
        edges = [tuple(el.split(")")) for el in edges_str]

        parents = {b: a for a, b in edges}
        nodes = set(n for e in edges for n in e)

        @lru_cache(maxsize=10_000)
        def _get_depth(node):
            if node == "COM":
                return 0
            else:
                return 1 + _get_depth(parents[node])
        
        return sum(_get_depth(node) for node in nodes)
