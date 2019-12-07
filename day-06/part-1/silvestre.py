from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        edges_str = s.split("\n")
        edges = [tuple(el.split(")")) for el in edges_str]

        tree = self.build_tree(edges, "COM")
        return self.count_depth(tree)

    @staticmethod
    def build_tree(edges, root_node):

        def _build_tree(edges, node, current_depth):
            children = [
                _build_tree(edges, node_to, current_depth+1) 
                for node_from, node_to in edges 
                if node_from == node
            ]
            return {
                "node": node,
                "children": children,
                "depth": current_depth
            }
        
        return _build_tree(edges, root_node, 0)

    def count_depth(self, tree):
        return tree["depth"] + sum(self.count_depth(child) for child in tree["children"])