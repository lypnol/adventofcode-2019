from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        pairs = [tuple(line.split(")")) for line in s.splitlines()]
        idx, com_pair = [(idx, pair) for idx, pair in enumerate(pairs) if pair[0] == "COM"][0]
        paths_to_explore = [f"{com_pair[0]}/{com_pair[1]}"]
        paths = []
        pairs.pop(idx)
        while paths_to_explore:
            path_to_explore = paths_to_explore.pop(0)
            parent = path_to_explore.split("/")[-1]
            paths_to_explore.extend([f"{path_to_explore}/{second}" for first, second in pairs if parent == first])
            paths.append(path_to_explore)
        return sum(len(p.split("/")) - 1 for p in paths)
