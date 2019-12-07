from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    def run(self, s):
        edges_str = s.split("\n")
        edges = [tuple(el.split(")")) for el in edges_str]

        tree = self.build_tree(edges, "COM")
        return self.get_distance(tree, "YOU", "SAN") - 2

    @staticmethod
    def build_tree(edges, root_node):

        def _build_tree(edges, node):
            children = [
                _build_tree(edges, node_to) 
                for node_from, node_to in edges 
                if node_from == node
            ]
            return {
                "name": node,
                "children": children,
            }
        
        return _build_tree(edges, root_node)

    def get_distance(self, tree, node_from, node_to):
        node_from_parents = self.get_path(tree, node_from)
        node_to_parents = self.get_path(tree, node_to)
        nearest_parent = [i for i,j in zip(node_from_parents, node_to_parents) if i==j][-1]

        return (
            len(node_from_parents) - node_from_parents.index(nearest_parent) -1 +
            len(node_to_parents) - node_to_parents.index(nearest_parent) -1 
        )

    @staticmethod
    def get_path(tree, target_node):

        def _get_path(root, target_node, parents_list):
            parents_list.append(root["name"])

            if root["name"] == target_node:
                return True 
            elif any(_get_path(child, target_node, parents_list) for child in root["children"]):
                return True
            else:
                parents_list.pop(-1)
                return False
    
        parents_list = []
        _get_path(tree,target_node, parents_list)
        return parents_list


