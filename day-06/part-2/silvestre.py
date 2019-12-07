from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):
    def run(self, s):
        edges_str = s.split("\n")
        edges = [tuple(el.split(")")) for el in edges_str]

        parents = {b: a for a, b in edges}
        nodes = set(n for e in edges for n in e)

        def _get_path(node, arr):
            arr.append(node)
            if node == "COM":
                return arr
            else:
                return _get_path(parents[node], arr)
        
        node_from_path = []
        node_to_path = []
        _get_path("YOU", node_from_path)
        _get_path("SAN", node_to_path)
        node_from_path = node_from_path[::-1]
        node_to_path = node_to_path[::-1]

        nearest_parent = [i for i,j in zip(node_from_path, node_to_path) if i==j][-1]

        dist = (
            len(node_from_path) - node_from_path.index(nearest_parent) -1 +
            len(node_to_path) - node_to_path.index(nearest_parent) -1 
        )

        return dist - 2
