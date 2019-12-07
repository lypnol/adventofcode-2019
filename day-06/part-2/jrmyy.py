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

        you_path = [path for path in paths if path.split("/")[-1] == "YOU"][0].split("/")
        san_path = [path for path in paths if path.split("/")[-1] == "SAN"][0].split("/")
        i = 0
        while you_path[i] == san_path[i]:
            i += 1

        return len(you_path) + len(san_path) - 2 * (i + 1)
